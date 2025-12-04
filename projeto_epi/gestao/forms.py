from django import forms
from .models import Colaborador, Equipamento, Emprestimo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'matricula', 'cargo'] # Campos que aparecerão no form
        # Você pode adicionar widgets para estilização (ex: com Bootstrap)
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EquipamentoForm(forms.ModelForm):

    class Meta:
        model = Equipamento
        # Por enquanto, vamos incluir todos os campos no form
        fields = ['nome', 'ca', 'quantidade_total', 'quantidade_disponivel', 'data_validade']

        # (Opcional, mas bom para os alunos) Widgets para melhorar a interface
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ca': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade_disponivel': forms.NumberInput(attrs={'class': 'form-control'}),
            # Usar um widget de Data facilita a seleção
            'data_validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
        }

# 1. Formulário de CRIAÇÃO de Usuário
# Usamos o UserCreationForm como base para cuidar da senha
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Adicionamos campos que queremos no formulário de criação
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'is_staff')
        # 'is_staff' permite que este usuário acesse o /admin/

        # (Opcional) Adiciona classes de CSS
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        # Os campos de senha já são tratados pelo UserCreationForm

# 2. Formulário de ATUALIZAÇÃO de Usuário
# Aqui usamos um ModelForm normal, pois NÃO vamos alterar a senha
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # Campos que podem ser editados
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EmprestimoForm(forms.ModelForm):

    # Este __init__ é a "mágica" para filtrar o estoque
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filtramos o queryset do campo 'equipamento'
        # para mostrar APENAS os EPIs com estoque > 0
        self.fields['equipamento'].queryset = Equipamento.objects.filter(
            quantidade_disponivel__gt=0
        )

        # Também filtramos para mostrar apenas colaboradores ativos
        self.fields['colaborador'].queryset = Colaborador.objects.filter(
            ativo=True
        )

    class Meta:
        model = Emprestimo
        # O usuário só precisa selecionar QUEM e O QUÊ.
        # As datas e o estoque serão tratados na View.
        fields = ['colaborador', 'equipamento', 'observacao']

        widgets = {
            'colaborador': forms.Select(attrs={'class': 'form-control'}),
            'equipamento': forms.Select(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


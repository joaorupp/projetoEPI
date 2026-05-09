from django import forms
from .models import Colaborador, Equipamento, Emprestimo, Usuario # Importa seu Usuario
from django.contrib.auth.forms import UserCreationForm

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador
        fields = ['nome', 'matricula', 'cargo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
        }
# --- EQUIPAMENTO ---
class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'ca', 'quantidade_total', 'quantidade_disponivel', 'data_validade']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ca': forms.TextInput(attrs={'class': 'form-control'}),
            'quantidade_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantidade_disponivel': forms.NumberInput(attrs={'class': 'form-control'}),
            'data_validade': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
        }

# --- USUÁRIOS (ATV:02 - PERFIS) ---
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario # Alterado para seu modelo customizado
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'perfil') # Adicionado perfil

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'perfil', 'is_active']

# --- MOVIMENTAÇÃO (ATV:05 - TRAVA DE ESTOQUE) ---
class EmprestimoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostra apenas EPIs que tenham pelo menos 1 no estoque
        self.fields['equipamento'].queryset = Equipamento.objects.filter(quantidade_disponivel__gt=0)
        self.fields['colaborador'].queryset = Colaborador.objects.filter(ativo=True)

    class Meta:
        model = Emprestimo
        # Adicionado 'quantidade_retirada' para que o aluno possa testar a trava
        fields = ['colaborador', 'equipamento', 'quantidade_retirada', 'observacao']
        widgets = {
            'colaborador': forms.Select(attrs={'class': 'form-control'}),
            'equipamento': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_retirada': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
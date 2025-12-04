from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, View)
from .models import Colaborador, Equipamento, Emprestimo
from django.utils import timezone
from .forms import (
    ColaboradorForm, EquipamentoForm,
    CustomUserCreationForm, UserUpdateForm, EmprestimoForm
)
from django.contrib.auth.models import User
def home(request):
    return render(request, "index.html")
# Read (Listar)
class ColaboradorListView(ListView):
    model = Colaborador
    template_name = 'gestao/colaborador_list.html'
    context_object_name = 'colaboradores' # Nome da variável na lista
    queryset = Colaborador.objects.filter(ativo=True) # Apenas colaboradores ativos

# Create (Criar)
class ColaboradorCreateView(CreateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'gestao/colaborador_form.html'
    success_url = reverse_lazy('colaborador_list') # Para onde vai após criar

# Update (Atualizar)
class ColaboradorUpdateView(UpdateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'gestao/colaborador_form.html'
    success_url = reverse_lazy('colaborador_list')

# Delete (Excluir)
class ColaboradorDeleteView(DeleteView):
    model = Colaborador
    template_name = 'gestao/colaborador_confirm_delete.html'
    success_url = reverse_lazy('colaborador_list')

# Read (Listar EPIs)
class EquipamentoListView(ListView):
    model = Equipamento
    template_name = 'gestao/equipamento_list.html'
    context_object_name = 'equipamentos'

# Create (Criar EPI)
class EquipamentoCreateView(CreateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = 'gestao/equipamento_form.html'
    success_url = reverse_lazy('equipamento_list')

# Update (Atualizar EPI)
class EquipamentoUpdateView(UpdateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = 'gestao/equipamento_form.html'
    success_url = reverse_lazy('equipamento_list')

# Delete (Excluir EPI)
class EquipamentoDeleteView(DeleteView):
    model = Equipamento
    template_name = 'gestao/equipamento_confirm_delete.html'
    success_url = reverse_lazy('equipamento_list')

# Read (Listar Usuários)
class UserListView(ListView):
    model = User
    template_name = 'gestao/user_list.html'
    context_object_name = 'usuarios'
    # Boa prática: não listar o superusuário se houver muitos
    queryset = User.objects.filter(is_superuser=False)

# Create (Criar Usuário)
class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm # <- Usando o form especial
    template_name = 'gestao/user_form.html'
    success_url = reverse_lazy('user_list')

# Update (Atualizar Usuário)
class UserUpdateView(UpdateView):
    model = User
    form_class = UserUpdateForm # <- Usando o form de atualização
    template_name = 'gestao/user_form.html'
    success_url = reverse_lazy('user_list')

# Delete (Excluir Usuário)
class UserDeleteView(DeleteView):
    model = User
    template_name = 'gestao/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

class EmprestimoListView(ListView):
    model = Emprestimo
    template_name = 'gestao/emprestimo_list.html'
    context_object_name = 'emprestimos'

    # Vamos mostrar apenas os empréstimos ATIVOS (não devolvidos)
    def get_queryset(self):
        return Emprestimo.objects.filter(data_devolucao__isnull=True)

# Create (Criar Empréstimo)
class EmprestimoCreateView(CreateView):

    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'gestao/emprestimo_form.html'
    success_url = reverse_lazy('emprestimo_list')

    # ---- AQUI ESTÁ A LÓGICA DE NEGÓCIO ----
    # Sobrescrevemos o método que é chamado quando o formulário é válido
    def form_valid(self, form):
        # 1. Pega o objeto do formulário, mas não salva no banco ainda
        emprestimo = form.save(commit=False)

        # 2. Define a data do empréstimo (já que não pedimos no form)
        emprestimo.data_emprestimo = timezone.now()

        # 3. Pega o EPI que foi selecionado
        epi = emprestimo.equipamento

        # 4. DECREMENTA O ESTOQUE
        # (Já checamos se é > 0 no Formulário,
        #  mas uma dupla checagem é segura)
        if epi.quantidade_disponivel > 0:
            epi.quantidade_disponivel -= 1
            epi.save() # Salva a mudança no EPI

            # 5. Agora sim, salva o Empréstimo no banco
            emprestimo.save()
        else:
            # Se algo deu errado (ex: estoque acabou durante o preenchimento)
            form.add_error('equipamento', 'Este EPI não está mais disponível em estoque.')
            return self.form_invalid(form)

        # 6. Redireciona para a success_url (a lista)
        return super().form_valid(form)

class EmprestimoDevolucaoView(View):
    # Esta view não tem template (GET), ela só processa o POST

    def post(self, request, *args, **kwargs):
        # 1. 'pk' é o ID do Empréstimo, que virá pela URL
        emprestimo_pk = self.kwargs.get('pk')

        # 2. Busca o empréstimo ou retorna erro 404
        emprestimo = get_object_or_404(Emprestimo, pk=emprestimo_pk)

        # 3. LÓGICA DE NEGÓCIO: Só devolve se não estiver devolvido
        if emprestimo.data_devolucao is None:
            # 4. Define a data da devolução
            emprestimo.data_devolucao = timezone.now()
            emprestimo.save()

            # 5. LÓGICA DE ESTOQUE: Incrementa a quantidade
            epi = emprestimo.equipamento
            epi.quantidade_disponivel += 1
            epi.save()

        # 6. Redireciona de volta para a lista de empréstimos ativos
        return redirect('emprestimo_list')



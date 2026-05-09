from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, View)
from .models import Colaborador, Equipamento, Emprestimo, Usuario # Importado o novo modelo Usuario
from django.utils import timezone
from .forms import (
    ColaboradorForm, EquipamentoForm,
    CustomUserCreationForm, UserUpdateForm, EmprestimoForm
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

# --- MIDDLEWARE DE PROTEÇÃO (ATV:02) ---
# Verifica se o usuário é Administrador para permitir DELETE
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.perfil == 'admin'

def home(request):
    return render(request, "gestao/index.html")

# --- COLABORADOR ---
class ColaboradorListView(LoginRequiredMixin, ListView):
    model = Colaborador
    template_name = 'gestao/colaborador_list.html'
    context_object_name = 'colaboradores'
    queryset = Colaborador.objects.filter(ativo=True)

class ColaboradorCreateView(LoginRequiredMixin, CreateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'gestao/colaborador_form.html'
    success_url = reverse_lazy('colaborador_list')

class ColaboradorUpdateView(LoginRequiredMixin, UpdateView):
    model = Colaborador
    form_class = ColaboradorForm
    template_name = 'gestao/colaborador_form.html'
    success_url = reverse_lazy('colaborador_list')

class ColaboradorDeleteView(AdminRequiredMixin, DeleteView): # Apenas Admin apaga (ATV:02)
    model = Colaborador
    template_name = 'gestao/colaborador_confirm_delete.html'
    success_url = reverse_lazy('colaborador_list')

# --- EQUIPAMENTO (EPI) ---
class EquipamentoListView(LoginRequiredMixin, ListView):
    model = Equipamento
    template_name = 'gestao/equipamento_list.html'
    context_object_name = 'equipamentos'

    # ATV:03 - Filtros por nome e paginação (Lógica simplificada para a view)
    def get_queryset(self):
        queryset = super().get_queryset()
        nome = self.request.GET.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        return queryset

class EquipamentoCreateView(LoginRequiredMixin, CreateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = 'gestao/equipamento_form.html'
    success_url = reverse_lazy('equipamento_list')

class EquipamentoDeleteView(AdminRequiredMixin, DeleteView): # Apenas Admin (ATV:02)
    model = Equipamento
    template_name = 'gestao/equipamento_confirm_delete.html'
    success_url = reverse_lazy('equipamento_list')

# --- GESTÃO DE MOVIMENTAÇÃO / EMPRÉSTIMO ---
class EmprestimoListView(LoginRequiredMixin, ListView):
    model = Emprestimo
    template_name = 'gestao/emprestimo_list.html'
    context_object_name = 'emprestimos'

    def get_queryset(self):
        return Emprestimo.objects.filter(data_devolucao__isnull=True)

class EmprestimoCreateView(LoginRequiredMixin, CreateView):
    model = Emprestimo
    form_class = EmprestimoForm
    template_name = 'gestao/emprestimo_form.html'
    success_url = reverse_lazy('emprestimo_list')

    # ---- ATV:04 e ATV:05 - REGRAS DE NEGÓCIO E TRAVA DE ESTOQUE ----
    def form_valid(self, form):
        movimentacao = form.save(commit=False)
        epi = movimentacao.equipamento
        qtd_solicitada = movimentacao.quantidade_retirada # Usando o campo novo do models

        # 1. VALIDAÇÃO DE ESTOQUE (Critério de Aceite da Prova)
        if qtd_solicitada > epi.quantidade_disponivel:
            # Mensagem exata exigida pelo enunciado da prova 
            erro_msg = f"Saída não permitida: estoque insuficiente. Disponível: {epi.quantidade_disponivel}. Solicitado: {qtd_solicitada}."
            form.add_error('quantidade_retirada', erro_msg)
            return self.form_invalid(form)

        # 2. RASTREABILIDADE (ATV:04)
        movimentacao.usuario_responsavel = self.request.user # Grava o usuário logado 
        movimentacao.data_emprestimo = timezone.now()
        
        # 3. ATUALIZAÇÃO DO SALDO
        epi.quantidade_disponivel -= qtd_solicitada
        epi.save()

        movimentacao.save()
        return super().form_valid(form)

class EmprestimoDevolucaoView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        emprestimo = get_object_or_404(Emprestimo, pk=self.kwargs.get('pk'))
        if emprestimo.data_devolucao is None:
            emprestimo.data_devolucao = timezone.now()
            emprestimo.save()

            epi = emprestimo.equipamento
            epi.quantidade_disponivel += emprestimo.quantidade_retirada
            epi.save()
        return redirect('emprestimo_list')
    
class EquipamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipamento
    form_class = EquipamentoForm
    template_name = 'gestao/equipamento_form.html'
    success_url = reverse_lazy('equipamento_list')

class UserListView(AdminRequiredMixin, ListView):
    model = Usuario
    template_name = 'gestao/user_list.html'
    context_object_name = 'usuarios'

class UserCreateView(AdminRequiredMixin, CreateView):
    model = Usuario
    form_class = CustomUserCreationForm
    template_name = 'gestao/user_form.html'
    success_url = reverse_lazy('user_list')

class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = Usuario
    form_class = UserUpdateForm
    template_name = 'gestao/user_form.html'
    success_url = reverse_lazy('user_list')

class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'gestao/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')
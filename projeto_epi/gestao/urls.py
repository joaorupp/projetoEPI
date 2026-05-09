from django.urls import path
from django.contrib.auth import views as auth_views # Import importante para login/logout
from .views import (
    ColaboradorListView, ColaboradorCreateView,
    ColaboradorUpdateView, ColaboradorDeleteView,
    EquipamentoListView, EquipamentoCreateView,
    EquipamentoUpdateView, EquipamentoDeleteView,
    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
    EmprestimoListView, EmprestimoCreateView,
    EmprestimoDevolucaoView, home
)

urlpatterns = [
    path('', home, name='home'),
    
    # --- AUTENTICAÇÃO (ATV:02) ---
    path('login/', auth_views.LoginView.as_view(template_name='gestao/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # --- COLABORADORES ---
    path('colaboradores/', ColaboradorListView.as_view(), name='colaborador_list'),
    path('colaboradores/novo/', ColaboradorCreateView.as_view(), name='colaborador_create'),
    path('colaboradores/<int:pk>/editar/', ColaboradorUpdateView.as_view(), name='colaborador_update'),
    path('colaboradores/<int:pk>/excluir/', ColaboradorDeleteView.as_view(), name='colaborador_delete'),

    # --- EQUIPAMENTOS ---
    path('equipamentos/', EquipamentoListView.as_view(), name='equipamento_list'),
    path('equipamentos/novo/', EquipamentoCreateView.as_view(), name='equipamento_create'),
    path('equipamentos/<int:pk>/editar/', EquipamentoUpdateView.as_view(), name='equipamento_update'),
    path('equipamentos/<int:pk>/excluir/', EquipamentoDeleteView.as_view(), name='equipamento_delete'),

    # --- USUÁRIOS ---
    path('usuarios/', UserListView.as_view(), name='user_list'),
    path('usuarios/novo/', UserCreateView.as_view(), name='user_create'),
    path('usuarios/<int:pk>/editar/', UserUpdateView.as_view(), name='user_update'),
    path('usuarios/<int:pk>/excluir/', UserDeleteView.as_view(), name='user_delete'),

    # --- MOVIMENTAÇÕES ---
    path('emprestimos/', EmprestimoListView.as_view(), name='emprestimo_list'),
    path('emprestimos/novo/', EmprestimoCreateView.as_view(), name='emprestimo_create'),
    path('emprestimos/<int:pk>/devolver/', EmprestimoDevolucaoView.as_view(), name='emprestimo_devolver'),
]
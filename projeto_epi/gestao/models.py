from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser # Importação necessária para o novo modelo de usuário

# 1. ATUALIZAÇÃO: Modelo de Usuário Customizado para Gestão de Perfis
# Atende ao requisito de ter Administrador e Operador com permissões específicas.
class Usuario(AbstractUser):
    PERFIS = (
        ('admin', 'Administrador do Sistema'),
        ('operador', 'Operador de Almoxarifado'),
    )
    perfil = models.CharField(
        max_length=10, 
        choices=PERFIS, 
        default='operador',
        verbose_name="Perfil de Acesso"
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

class Colaborador(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20, unique=True, verbose_name="Matrícula")
    cargo = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

class Equipamento(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome do Equipamento")
    ca = models.CharField(max_length=50, verbose_name="C.A. (Certificado de Aprovação)")
    
    # IMPORTANTE: Campos para a regra de negócio de estoque (Atividade 04 e 05)
    quantidade_total = models.PositiveIntegerField(default=0, verbose_name="Quantidade Total")
    quantidade_disponivel = models.PositiveIntegerField(default=0, verbose_name="Quantidade Disponível")
    
    data_validade = models.DateField(verbose_name="Data de Validade")

    def __str__(self):
        return f"{self.nome} (C.A: {self.ca}) - Disponível: {self.quantidade_disponivel}"

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

class Emprestimo(models.Model):
    colaborador = models.ForeignKey(
        Colaborador, 
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )
    equipamento = models.ForeignKey(
        Equipamento, 
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )

    # 2. ATUALIZAÇÃO: Rastreabilidade (Atividade 04)
    # Adicionado campo para registrar quem realizou a operação.
    usuario_responsavel = models.ForeignKey(
    'Usuario', 
    on_delete=models.SET_NULL, 
    null=True,   # Permite que registros antigos fiquem vazios
    blank=True,  # Permite que o formulário ignore este campo
    verbose_name="Responsável pela Saída"
)

    # Campo de data e hora formatado conforme exigência (25-12-2025 16:50)
    data_emprestimo = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Data do Empréstimo"
    )

    data_devolucao = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Data de Devolução"
    )

    # Campo para registrar a quantidade retirada para validação do estoque
    quantidade_retirada = models.PositiveIntegerField(default=1, verbose_name="Qtd. Retirada")

    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")

    def __str__(self):
        status = "Ativo" if self.data_devolucao is None else "Devolvido"
        return f"{self.equipamento.nome} para {self.colaborador.nome} ({status})"

    class Meta:
        verbose_name = "Empréstimo/Movimentação"
        verbose_name_plural = "Empréstimos/Movimentações"
        ordering = ['-data_emprestimo']
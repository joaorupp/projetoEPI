from django.db import models
from django.utils import timezone

# Create your models here.

class Colaborador(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20, unique=True, verbose_name="Matrícula")
    cargo = models.CharField(max_length=100)
    # Adicionamos um campo 'ativo' que é uma boa prática
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.matricula})"

    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

class Equipamento(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome do Equipamento")

    # O "CA" é o Certificado de Aprovação, essencial para EPIs
    ca = models.CharField(max_length=50, verbose_name="C.A. (Certificado de Aprovação)")

    # Vamos controlar a quantidade em estoque
    quantidade_total = models.PositiveIntegerField(default=0, verbose_name="Quantidade Total")

    # Boa prática: controlar o que está disponível
    quantidade_disponivel = models.PositiveIntegerField(default=0, verbose_name="Quantidade Disponível")

    # Data de validade do C.A. ou do equipamento
    data_validade = models.DateField(verbose_name="Data de Validade")

    def __str__(self):
        return f"{self.nome} (C.A: {self.ca})"

    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"

class Emprestimo(models.Model):
    # RELACIONAMENTOS (Chaves Estrangeiras)

    # 'on_delete=models.PROTECT' impede que um colaborador seja
    # excluído se tiver empréstimos ativos.
    colaborador = models.ForeignKey(
        Colaborador, 
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )

    # 'on_delete=models.PROTECT' impede que um EPI seja excluído
    # se estiver emprestado.
    equipamento = models.ForeignKey(
        Equipamento, 
        on_delete=models.PROTECT,
        related_name='emprestimos'
    )

    # INFORMAÇÕES DO EMPRÉSTIMO
    data_emprestimo = models.DateTimeField(
        default=timezone.now, 
        verbose_name="Data do Empréstimo"
    )

    # Este campo é a chave:
    # Se for NULO, o empréstimo está ATIVO.
    # Se tiver uma data, o EPI foi DEVOLVIDO.
    data_devolucao = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Data de Devolução"
    )

    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")

    def __str__(self):
        # Mostra se está ativo ou devolvido
        status = "Ativo" if self.data_devolucao is None else "Devolvido"
        return f"{self.equipamento.nome} para {self.colaborador.nome} ({status})"

    class Meta:
        verbose_name = "Empréstimo"
        verbose_name_plural = "Empréstimos"
        # Garante que os mais recentes apareçam primeiro
        ordering = ['-data_emprestimo']

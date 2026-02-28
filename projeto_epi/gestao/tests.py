from django.test import TestCase
import pytest
from datetime import date
from .models import Equipamento  # Importamos o modelo!

@pytest.mark.django_db
def test_criar_equipamento():
    # 1. Ação: Criar o EPI no banco de dados de teste
    capacete = Equipamento.objects.create(
        nome="Capacete de Segurança",
        ca="12345",
        quantidade_total=10,
        quantidade_disponivel=10,
        data_validade=date(2027, 12, 31)
    )

    # 2. Verificação (Assert): Garantir que ele foi salvo com os dados corretos
    assert capacete.nome == "Capacete de Segurança"
    assert capacete.quantidade_disponivel == 10
    
    # 3. Verificação Extra: Garantir que realmente existe 1 item salvo no banco
    assert Equipamento.objects.count() == 1

# Create your tests here.

def test_configuracao_inicial():
    assert 1 + 1 == 1





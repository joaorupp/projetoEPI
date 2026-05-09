import os
import django

# Configura o ambiente do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_epi.settings')
django.setup()

from gestao.models import Usuario, Colaborador, Equipamento
from django.utils import timezone

def popular_banco():
    print("Iniciando carga de dados...")

    # 1. Criar Usuários (Se não existirem)
    if not Usuario.objects.filter(username='admin').exists():
        Usuario.objects.create_superuser('admin', 'admin@teste.com', 'admin123', perfil='admin')
        print("- Admin criado (user: admin, pass: admin123)")

    if not Usuario.objects.filter(username='operador').exists():
        Usuario.objects.create_user('operador', 'op@teste.com', 'op123', perfil='operador')
        print("- Operador criado (user: operador, pass: op123)")

    # 2. Criar Colaboradores
    colaboradores = [
        {'nome': 'João Silva', 'matricula': '1001', 'cargo': 'Eletricista'},
        {'nome': 'Maria Santos', 'matricula': '1002', 'cargo': 'Mecânico'},
        {'nome': 'Pedro Souza', 'matricula': '1003', 'cargo': 'Ajudante Geral'},
    ]
    for c in colaboradores:
        Colaborador.objects.get_or_create(matricula=c['matricula'], defaults=c)
    print("- Colaboradores criados.")

    # 3. Criar Equipamentos (EPIs)
    equipamentos = [
        {
            'nome': 'Capacete de Segurança', 
            'ca': '12345', 
            'quantidade_total': 50, 
            'quantidade_disponivel': 50, 
            'data_validade': '2027-12-31'
        },
        {
            'nome': 'Luva Nitrílica', 
            'ca': '67890', 
            'quantidade_total': 100, 
            'quantidade_disponivel': 100, 
            'data_validade': '2026-06-15'
        },
        {
            'nome': 'Bota com Biqueira', 
            'ca': '11223', 
            'quantidade_total': 30, 
            'quantidade_disponivel': 5, # Poucos disponíveis para testar trava
            'data_validade': '2028-01-01'
        },
    ]
    for e in equipamentos:
        Equipamento.objects.get_or_create(ca=e['ca'], defaults=e)
    print("- Equipamentos criados.")

    print("\nPronto! Banco de dados populado com sucesso.")

if __name__ == '__main__':
    popular_banco()
from django.contrib import admin
from .models import Colaborador, Equipamento

# Register your models here.

@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    # (Opcional, mas recomendado) Define o que aparece na lista
    list_display = ('nome', 'matricula', 'cargo', 'ativo')
    
    # (Opcional) Adiciona um campo de busca
    search_fields = ('nome', 'matricula')


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    # Campos que você quer ver na lista
    list_display = (
        'nome', 
        'ca', 
        'data_validade', 
        'quantidade_total', 
        'quantidade_disponivel'
    )
    # (Opcional) Adiciona um filtro prático pela data
    list_filter = ('data_validade',)
    # (Opcional) Adiciona busca por nome ou C.A.
    search_fields = ('nome', 'ca')
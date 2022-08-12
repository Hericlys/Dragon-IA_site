from django.contrib import admin
from .models import Chave


class ChaveAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'chave',
        'data_criacao',
        'data_expiracao',
    )

    list_display_links = (
        'usuario',
        'chave',
    )

    search_fields = [
        'usuario__username',
        'chave',
    ]


admin.site.register(Chave, ChaveAdmin)

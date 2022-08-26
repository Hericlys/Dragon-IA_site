from django.contrib import admin
from .models import Chave, Paridades


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


class ParidadesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'paridade',
        'put',
        'call',
    )

    list_display_links = (
        'paridade',
    )

    search_fields = [
        'paridade',
    ]


admin.site.register(Chave, ChaveAdmin)
admin.site.register(Paridades, ParidadesAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['username']
    list_display = ['username', 'name', 'is_active', ]
    fieldsets = (
        (
            _('Anmeldedaten'), 
            {'fields': ('username', 'password')}
        ),
        (_('Persönliche Informationen'), {'fields': ('name',)}),
        (
            _('Berechtigungen'),
            {'fields': ('groups', 'is_staff', 'is_verwaltung',
             'is_benutzerverwaltung', 'is_superuser')}
        ),
        (_('Aktiv'), {'fields': ('is_active',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Modul)
admin.site.register(models.Katastrophe)
admin.site.register(models.Gefahr)
admin.site.register(models.Massnahme)
admin.site.register(models.Rolle)
admin.site.register(models.Kontakt)
admin.site.register(models.Dokument)
admin.site.register(models.Fahrzeug)
admin.site.register(models.FahrzeugFoto)
admin.site.register(models.KMaterial)

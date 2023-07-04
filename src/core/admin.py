from django.contrib import admin
from .models import Modul
from django import forms
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext as _











# TEXT = 'Some text that we can include'
# class ModulAdmin(admin.ModelAdmin):
#     fieldsets = (
#         ('Section 1', {
#             'fields': ('bezeichnung',),
#             'description':'%s' % TEXT,
#         }),
#         ('Section 2', {
#             'fields': ('kuerzel', 'reihenfolge',),
#             'classes': ('collapse',),
#         })
#     )
# admin.site.register(Modul, ModulAdmin)

# models = django.apps.apps.get_models()
# print(models)

# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass

# admin.site.unregister(django.contrib.admin.models.LogEntry)
# admin.site.unregister(django.contrib.auth.models.Permission)
# admin.site.unregister(django.contrib.auth.models.Group)
# admin.site.unregister(django.contrib.contenttypes.models.ContentType)
# admin.site.unregister(django.contrib.sessions.models.Session)
# admin.site.unregister(rest_framework.authtoken.models.Token)
# admin.site.unregister(rest_framework.authtoken.models.TokenProxy)

class CoreAdminArea(admin.AdminSite):
    site_header = 'Core Admin Area'
    login_template = 'core/admin/login.html'

core_site = CoreAdminArea(name='CoreAdmin')

core_site.register(Modul)

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     ordering = ['username']
#     list_display = ['username', 'name', 'is_active', ]
#     fieldsets = (
#         (
#             _('Anmeldedaten'), 
#             {'fields': ('username', 'password')}
#         ),
#         (_('Persönliche Informationen'), {'fields': ('name',)}),
#         (
#             _('Berechtigungen'),
#             {'fields': ('groups', 'is_staff', 'is_verwaltung',
#              'is_benutzerverwaltung', 'is_superuser')}
#         ),
#         (_('Aktiv'), {'fields': ('is_active',)})
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'password1', 'password2')
#         }),
#     )


# admin.site.register(User, UserAdmin)
# admin.site.register(models.Modul)
# admin.site.register(models.Katastrophe)
# admin.site.register(models.Gefahr)
# admin.site.register(models.Massnahme)
# admin.site.register(models.Rolle)
# admin.site.register(models.Kontakt)
# admin.site.register(models.Dokument)
# admin.site.register(models.Fahrzeug)
# admin.site.register(models.FahrzeugFoto)
# admin.site.register(models.KMaterial)

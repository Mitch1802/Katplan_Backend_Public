from django.urls import path, include
from rest_framework.routers import DefaultRouter

from katplan import views


router = DefaultRouter()
# router.register('modul', views.ModulViewSet)
# router.register('katastrophe', views.KatastropheViewSet)
# router.register('gefahr', views.GefahrViewSet)
# router.register('massnahme', views.MassnahmeViewSet)
# router.register('rolle', views.RolleViewSet)
# router.register('kontakt', views.KontaktViewSet)
# router.register('dokument', views.DokumentViewSet)
# router.register('fahrzeug', views.FahrzeugViewSet)
# router.register('fahrzeugfoto', views.FahrzeugFotoViewSet)
# router.register('kmaterial', views.KMaterialViewSet)

app_name = 'katplan'

urlpatterns = [
    path('modul/', views.ModulViewSet.as_view(), name='modul'),
    path('katastrophe/', views.KatastropheViewSet.as_view(), name='katastrophe'),
    path('gefahr/', views.GefahrViewSet.as_view(), name='gefahr'),
    path('massnahme/', views.MassnahmeViewSet.as_view(), name='massnahme'),
    path('rolle/', views.RolleViewSet.as_view(), name='rolle'),
    path('kontakt/', views.KontaktViewSet.as_view(), name='kontakt'),
    path('dokument/', views.DokumentViewSet.as_view(), name='dokument'),
    path('fahrzeug/', views.FahrzeugViewSet.as_view(), name='fahrzeug'),
    path('fahrzeugfoto/', views.FahrzeugFotoViewSet.as_view(), name='fahrzeugfoto'),
    path('kmaterial/', views.KMaterialViewSet.as_view(), name='kmaterial'),
    path('', include(router.urls))
]

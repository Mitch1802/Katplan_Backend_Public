from django.urls import path, include
from rest_framework.routers import DefaultRouter

from katplan import views


router = DefaultRouter()
router.register('modul', views.ModulViewSet)
router.register('katastrophe', views.KatastropheViewSet)
router.register('gefahr', views.GefahrViewSet)
router.register('massnahme', views.MassnahmeViewSet)
router.register('rolle', views.RolleViewSet)
router.register('kontakt', views.KontaktViewSet)
router.register('dokument', views.DokumentViewSet)
router.register('fahrzeug', views.FahrzeugViewSet)
router.register('fahrzeugfoto', views.FahrzeugFotoViewSet)
router.register('kmaterial', views.KMaterialViewSet)

app_name = 'katplan'

urlpatterns = [
    path('', include(router.urls))
]

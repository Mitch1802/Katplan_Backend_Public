from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core.admin import core_site


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('coreadmin/', core_site.urls),
    path('api/user/', include('user.urls')),
    path('api/', include('katplan.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

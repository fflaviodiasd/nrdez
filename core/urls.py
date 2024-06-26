from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
   openapi.Info(
      title="Norma Regulamentar",
      default_version='v1',
      description="Este documento descreve os recursos disponíveis nesta API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="ffsilva@sfiec.org.br"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/', include('apps.accounts.urls')),
    path(r'api/', include('apps.companies.urls')),
    path(r'api/', include('apps.equipment.urls')),
    path(r'api/', include('apps.profiles.urls')),
    path(r'api/', include('apps.sectors.urls')),

    re_path(r'^(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

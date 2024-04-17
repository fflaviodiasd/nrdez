from django.contrib import admin
from django.urls import path, include
from apps.companies.views import CompanyViewSet
from apps.equipment.views import EquipmentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('company', CompanyViewSet, basename='Company')
router.register('equipment', EquipmentViewSet, basename='Equipment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]

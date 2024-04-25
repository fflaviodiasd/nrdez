from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import EmployeeDeleteViewSet


urlpatterns = [
    path('employees/<int:pk>/', EmployeeDeleteViewSet.as_view({'delete': 'destroy'}), name='employee-delete'),
]
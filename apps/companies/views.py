from rest_framework import viewsets
from apps.companies.models import Company
from apps.companies.serializer import CompanySerializer


# Create your views here.
class CompanyViewSet(viewsets.ModelViewSet):
    """Exibindo todos as Empresas"""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

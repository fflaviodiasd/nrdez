from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets

from .models import Sector
from apps.companies.models import Company
from .serializer import SectorSerializer

class SectorViewSet(ModelViewSet):
    serializer_class = SectorSerializer
    queryset = Sector.objects.all()

class CompanySectorViewSet(viewsets.ModelViewSet):
    """
    esse endpoint vai receber um id de uma company e listar os setores associados a ela.
    """
    serializer_class = SectorSerializer
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        company_id = self.kwargs['id']
        try:
            company = Company.objects.get(id=company_id)
            sectors = Sector.objects.filter(company=company)
            return sectors
        except Company.DoesNotExist:
            return Sector.objects.none()
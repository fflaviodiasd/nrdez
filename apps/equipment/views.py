from rest_framework import viewsets
from apps.equipment.models import Equipments
from apps.equipment.serializer import EquipmentSerializer

# Create your views here.
class EquipmentViewSet(viewsets.ModelViewSet):

    queryset = Equipments.objects.all()
    serializer_class = EquipmentSerializer
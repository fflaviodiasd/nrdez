from rest_framework import serializers
from apps.equipment.models import Equipments

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipments
        fields = '__all__'
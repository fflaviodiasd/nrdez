from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Employee
from apps.accounts.models import CustomUser
from .serializer import EmployeeSerializer
from django.shortcuts import get_object_or_404


class EmployeeDeleteViewSet(viewsets.ModelViewSet):
    """
    esse endpoint vai receber id de um funcionario, e deletar seu perfil emplooye, seu perfil user, e suas informações genericas.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def destroy(self, request, pk=None):
        try:
            instance = self.get_object()
            user = instance.user
            generic_profile = instance
            custom_user = get_object_or_404(CustomUser, pk=user.id)

            if user and generic_profile and custom_user:
                user.delete()
                generic_profile.delete()
                custom_user.delete()

                return Response({"message": "Employee, GenericProfile, and CustomUser deleted successfully."},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "Related objects not found."}, status=status.HTTP_404_NOT_FOUND)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)


from rest_framework import viewsets
from .models import Employee
from apps.accounts.models import CustomUser
from .serializer import EmployeeSerializer


class EmployeeDeleteViewSet(viewsets.ModelViewSet):
    """
    esse endpoint vai receber id de um funcionario, e deletar seu perfil emplooye, seu perfil user, e suas informações genericas.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


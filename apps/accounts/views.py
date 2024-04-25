from django.shortcuts import render
from rest_framework import viewsets, mixins
# Create your views here.
class RegisterNewUser(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Cadastra novo usuário na plataforma. O campo tipo representa o perfil do usuário, sendo:
    - 1: Administrador
    - 2: Funcionário
    - 3: Gestor de Contas
    - 4: Prestador
    - 5: Prestador ADM

    **Nota:** Este endpoint não permite o cadastro de usuários do tipo **funcionário**.
    Perfis de usuário do tipo Administrador não precisam enviar o campo company_id, enquanto os
    demais perfis sim, caso contrário, um erro será retornado.
    """
    serializer_class = RegisterNewUserSerializer

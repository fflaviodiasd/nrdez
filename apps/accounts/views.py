from datetime import datetime

from django_rest_passwordreset.signals import reset_password_token_created
from django.db.models.signals import post_save
from django_rest_passwordreset import views as passwordreset_view
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from django.dispatch import receiver
from rest_framework import viewsets, mixins


from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import permissions, status, viewsets, mixins
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from apps.accounts.serializer import *
from apps.accounts.models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated,]
    # http_method_names = ['get', 'patch', 'put', 'delete']


@method_decorator(name='create', decorator=swagger_auto_schema(
    responses={status.HTTP_200_OK: RegisterNewUserResponseSerializer}
))
class RegisterNewUser(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Cadastra novo usuário na plataforma. O campo tipo representa o perfil do usuário, sendo:
    - 1: Administrador
    - 2: Funcionário
    **Nota:** Este endpoint não permite o cadastro de usuários do tipo **funcionário**.
    Perfis de usuário do tipo Administrador não precisam enviar o campo company_id, enquanto os
    demais perfis sim, caso contrário, um erro será retornado.
    """
    serializer_class = RegisterNewUserSerializer


class RecoveryPasswordEmployeeView(APIView):
    """
    Altera a senha do usuário funcionário a partir de seus dados pessoais. <br>
    **Nota:** Este endpoint só é válido para os perfil Funcionário, pois não possui email vinculado.
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=RecoveryPasswordSerializer,
        responses={status.HTTP_200_OK: RecoveryPasswordResponseSerializer}
    )
    def post(self, request):
        serializer = RecoveryPasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['profile'].user

        if user.is_first_login:
            user.is_first_login = False
            user.first_access_date = datetime.now()

        user.password = make_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            data={
                'user': user.username,
                'new_password': serializer.validated_data['new_password']

            },
            status=status.HTTP_200_OK
        )


class BlacklistRefreshView(APIView):
    """
    Realiza o logout do usuário na plataforma, expirando o refresh token.
    """

    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
        except TokenError:
            return Response(data={'detail': 'Token is invalid or expired'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={'message': 'Sucess'}, status=status.HTTP_200_OK)


class TokenObtainPairViewCustom(TokenObtainPairView):
    """
    Autentica o usuário na plataforma através de suas credenciais de acesso.

    """
    permission_classes = [permissions.AllowAny, ]
    serializer_class = TokenObtainPairSerializerCustom


class TokenRefreshViewCustom(TokenRefreshView):
    """
    Atualiza token de acesso. Quando o access token é expirado, este endpoint deve ser utilizado
    para realizar a atualização do token e manter o usuário autenticado.
    """
    pass


class EmailRecoveryPassword(passwordreset_view.ResetPasswordRequestToken):
    """
    Envia email contendo informações de alteração de senha do usuário. <br>
    **Nota:** Este endpoint só é válido para os seguintes perfis de usuários:
    Administrador, Prestador e Gestor de Contas, pois possuem email vinculados.
    """

    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
        user = reset_password_token.user
        send_email_task.delay(user.id, reset_password_token.key)


class ConfirmRecoveryPassword(passwordreset_view.ResetPasswordConfirm):
    """
    Altera a senha do usuário. Após o envio do email, o usuário receberá um token de validação.
    Este token deve ser passado juntamente com a nova senha para que a alteração seja realizada. e troca a flag de is_first_login para false <br>
    **Nota:** Este endpoint só é válido para os seguintes perfis de usuários:
    Administrador, Prestador e Gestor de Contas, pois possuem email vinculados.
    """

    @receiver(post_save, sender=CustomUser)
    def change_is_first_login_user(sender, **kwargs):
        user = kwargs.get('instance', None)
        if user.is_first_login:
            user.is_first_login = False
            user.first_access_date = datetime.now()
            user.save()
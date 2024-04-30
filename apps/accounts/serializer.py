from apps.profiles.models import GenericProfile
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db import transaction
from apps.accounts.models import *
from apps.accounts.services import *
from apps.profiles.services import create_profile
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    RefreshToken,
)



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','password','type','profile']

class RegisterNewUserSerializer(serializers.Serializer):
    # TODO - Aplicar internacionalização (translation)
    company_id = serializers.IntegerField(required=False)
    type = serializers.IntegerField(required=True, write_only=True)
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, write_only=True)

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("This email is already in use."))
        return value

    @transaction.atomic
    def create(self, validate_data, **kwargs):
        self.gen_password = CustomUser.objects.make_random_password()
        username = make_username(validate_data['name'])

        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError(_('Username already exists.'))

        if validate_data['type'] in [4, 5]:
            is_first_access_user = True
        else:
            is_first_access_user = False

        if validate_data['type'] == 1:
            is_first_login = False
        else:
            is_first_login = True

        user = CustomUser.objects.create(
            username=username,
            password=make_password(self.gen_password),
            email=validate_data['email'],
            type=validate_data['type'],
            is_first_access_user=is_first_access_user,  # Defina o valor com base na verificação acima
            is_first_login=is_first_login
        )

        profile = create_profile(user, validate_data)
        return profile


class RegisterNewUserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    company_id = serializers.IntegerField(required=False)
    type = serializers.IntegerField()
    username = serializers.CharField()
    password = serializers.CharField()


class RecoveryPasswordSerializer(serializers.Serializer):
    cpf = serializers.CharField(max_length=30)
    birth_date = serializers.DateField()
    new_password = serializers.CharField(max_length=30)

    def validate(self, data):
        profile = GenericProfile.objects.all().filter(cpf=data['cpf'], birth_date=data['birth_date']).order_by(
            'user__first_access_date').first()

        if not profile:
            raise serializers.ValidationError({"details": _("User not found")})

        data['profile'] = profile

        return data


class RecoveryPasswordResponseSerializer(serializers.Serializer):
    user = serializers.CharField(max_length=30)
    new_password = serializers.CharField(max_length=30)


class TokenObtainPairSerializerCustom(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        # Retorna informações do usuário juntamente com os tokens
        serializer = TokenUserSerializer(self.user)
        data['user'] = serializer.data
        return data


class TokenUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.IntegerField()
    name = serializers.CharField(source='profile.name')
    is_first_login = serializers.BooleanField(read_only=True)
    is_first_access_user = serializers.BooleanField(read_only=True)
    company = serializers.SerializerMethodField()
    is_first_access_company = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(read_only=True)

    def get_company(self, instance):

        if isAdministrator(instance):
            return None

        profile = get_profile(instance.profile, instance.type)
        return profile.company.id

    def get_is_first_access_company(self, instance):

        if isAdministrator(instance):
            return None

        profile = get_profile(instance.profile, instance.type)
        return profile.company.is_first_access_company


class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
    user = TokenUserSerializer()


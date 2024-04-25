from apps.profiles.models import GenericProfile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db import transaction
from apps.accounts.models import CustomUser
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
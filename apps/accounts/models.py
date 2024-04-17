from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    TYPE_CHOICES = (
        (1, 'Administrador'),
        (2, 'Funcionário'),
    )

    tipo = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=1)
    is_first_login = models.BooleanField(default=True)
    is_first_access_user= models.BooleanField(default=True)
    first_access_date = models.DateField(null=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Usuários"

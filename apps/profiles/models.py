from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from apps.sectors.models import Sector
from apps.accounts.models import CustomUser
from apps.companies.models import Company
from apps.accounts.services import isEmployee



class GenericProfile(models.Model):
    user = models.OneToOneField(CustomUser, null=True, on_delete=models.CASCADE, related_name='profile')
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    fone = models.CharField(max_length=16, null=True, blank=True)
    endereco = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=4, null=True, blank=True)
    complemento = models.CharField(max_length=80, null=True, blank=True)
    bairro = models.CharField(max_length=150, null=True, blank=True)
    cidade = models.CharField(max_length=150, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self) -> str:
        return self.usuario.username


# Signals para garantir que funcionário tenha cpf e data de nascimento registrado
@receiver(pre_save, sender=GenericProfile)
def valid_order(sender, instance, **kwargs):
    if isEmployee(instance.user):
        if not instance.cpf or not instance.birth_date:
            raise TypeError(_("CPF and Date of Birth are required"))


class Employee(GenericProfile):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employee_company')
    setor = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True)
    job = models.CharField(max_length=100, null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)


class Administrador(GenericProfile):
    pass


class AccountManager(GenericProfile):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


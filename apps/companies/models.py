from django.db import models

# Create your models here.

class Company(models.Model):
    nome_empresa = models.CharField(max_length=30)
    nome_fantasia = models.CharField(max_length=30)
    cnpj = models.CharField(max_length=30, blank=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.nome_empresa
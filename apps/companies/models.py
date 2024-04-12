from django.db import models

# Create your models here.

class Company(models.Model):
    nome = models.CharField(max_length=30)
    cnpj = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=30, blank=True)
    telefone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name
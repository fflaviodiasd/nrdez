from django.db import models

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=30)
    cnpj = models.CharField(max_length=30, blank=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name
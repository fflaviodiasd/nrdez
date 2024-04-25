from django.db import models

from apps.companies.models import Company


class Sector(models.Model):
    nome = models.CharField( max_length=50)

    company = models.ForeignKey(Company, related_name='setores', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome
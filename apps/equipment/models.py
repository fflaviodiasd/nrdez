from django.db import models

# Create your models here.
class Equipments(models.Model):
    CONTROLE = (
        ('AF', 'Aferição'),
        ('CA', 'Calibração'),
        ('CT', 'Controle'),
        ('EN', 'Ensaio'),
        ('IN', 'Inspeção')
    )

    SITUACAO = (
        ('FO', 'Fora de Operação'),
        ('NA', 'N/A'),
        ('OK', 'OK'),
        ('PR', 'Programar'),
        ('VE', 'Vencido')
    )

    equipmento_id = models.AutoField(primary_key=True)
    equipmento_name = models.CharField(max_length=10, blank=False, null=False)
    patrimonio = models.IntegerField(blank=True, null=True)
    numero_serie = models.IntegerField(blank=True, null=True)
    marca = models.CharField(max_length=10, blank=True, null=True)
    modelo = models.CharField(max_length=10, blank=True, null=True)
    controle = models.CharField(max_length=2, choices=CONTROLE, blank=True, null=False)
    faixa_equip = models.IntegerField(blank=True, null=True)
    utilizacao = models.CharField(max_length=100, blank=True, null=True)
    observacoes = models.TextField(max_length=100, blank=True, null=True)
    processo_calibraço = models.TextField(max_length=30, blank=True, null=True)
    situacao = models.CharField(max_length=2, choices=SITUACAO, blank=True, null=False)
    frequneciao = models.IntegerField(blank=True, null=True)
    proxima_calibracao = models.DateField()

    def __str__(self):
        return self.equipmento_name
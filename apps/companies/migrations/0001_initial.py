# Generated by Django 4.0 on 2024-04-18 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_empresa', models.CharField(max_length=30)),
                ('nome_fantasia', models.CharField(max_length=30)),
                ('cnpj', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address')),
                ('telefone', models.CharField(blank=True, max_length=10)),
            ],
        ),
    ]

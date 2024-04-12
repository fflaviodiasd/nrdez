from django.contrib import admin
from apps.companies.models import Company
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cnpj', 'email', 'telefone' )
    list_display_links = ('id', 'nome')
    search_fields = ('nome', 'cnpj')
    list_per_page = 20

admin.site.register(Company, CompanyAdmin)
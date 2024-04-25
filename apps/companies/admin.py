from django.contrib import admin
from apps.companies.models import Company
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome_empresa', 'nome_fantasia', 'cnpj')
    list_display_links = ('id', 'nome_empresa')
    list_filter = ('id', 'cnpj')
    list_per_page = 20


admin.site.register(Company, CompanyAdmin)
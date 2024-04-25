from django.contrib import admin

from .models import Sector

class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'company',)
    list_display_links = ('id', 'nome', 'company',)

admin.site.register(Sector, SectorAdmin)

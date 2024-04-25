from django.contrib import admin
from .models import *

admin.site.register(GenericProfile)
admin.site.register(Employee)
admin.site.register(Administrador)
admin.site.register(AccountManager)
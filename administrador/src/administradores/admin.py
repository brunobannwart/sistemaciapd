from django.contrib import admin

# Register your models here.
from .models import Administrador

admin.site.site_header = "Administrativo"
admin.site.site_title = "Vitalitá"
admin.site.index_title = "Gerenciamento do Vitalitá"

admin.site.register(Administrador)
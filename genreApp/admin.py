from django.contrib import admin
from .models import demoModel,Song
# Register your models here.

admin.site.register(demoModel)
admin.site.register(Song)
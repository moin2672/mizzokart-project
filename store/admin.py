from django.contrib import admin

from . import models

class StoreAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(models.Product, StoreAdmin)

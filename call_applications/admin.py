from django.contrib import admin
from .models import CallForApplication

class CallForApplicationAdmin(admin.ModelAdmin):
    pass

admin.site.register(CallForApplication, CallForApplicationAdmin)
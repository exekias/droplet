from django.contrib import admin
from models import ModuleInfo


class AuthorAdmin(admin.ModelAdmin):
    admin.site.register(ModuleInfo)

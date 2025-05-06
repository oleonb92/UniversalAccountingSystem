from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

User = get_user_model()

# Solo registramos si aún no ha sido registrado
try:
    admin.site.register(User, BaseUserAdmin)
except admin.sites.AlreadyRegistered:
    pass
from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'created', 'date_joined', 'last_login']

admin.site.register(User, UserAdmin)

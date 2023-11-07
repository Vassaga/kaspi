from django.contrib import admin

# Register your models here.

from auths.models import (
    MyUser,
)

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['number', 'fio', 'is_staff', 'is_active',  'id']
    list_filter = ['is_staff']
    ordering = ['id', 'number', 'fio']
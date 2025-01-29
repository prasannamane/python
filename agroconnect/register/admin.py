from django.contrib import admin
from .models import Register
 
# Register your models here.
@admin.register(Register)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'email', 'mobile', 'first_name', 'last_name']

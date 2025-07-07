from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verified', 'is_staff', 'date_joined')
    list_filter = ('is_verified', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
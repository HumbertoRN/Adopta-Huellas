from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# USER
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'shelter', 'is_staff', 'created_at')
    list_filter = ('role', 'shelter', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Datos extra', {'fields': ('phone', 'role', 'shelter')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Datos extra', {'fields': ('email', 'phone', 'role', 'shelter')}),
    )

# SHELTER
from .models import Shelter

@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'created_at')
    search_fields = ('name', 'address')

# PET
from .models import Pet

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'shelter', 'adoption_status', 'created_at')
    list_filter = ('species', 'adoption_status', 'gender', 'size', 'shelter')
    search_fields = ('name',)
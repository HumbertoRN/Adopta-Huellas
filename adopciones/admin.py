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

# ADOPTION_REQUEST
from .models import AdoptionRequest

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pet', 'status', 'request_date')
    list_filter = ('status', 'request_date')
    search_fields = ('user__username', 'pet__name')

# ADOPTION
from .models import Adoption

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'adoption_date')
    list_filter = ('adoption_date',)
    search_fields = ('request__user__username', 'request__pet__name')

# FAVORITE
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'created_at')
    search_fields = ('user__username', 'pet__name')

# PET_IMAGE
from .models import PetImage

@admin.register(PetImage)
class PetImageAdmin(admin.ModelAdmin):
    list_display = ('pet', 'is_primary', 'created_at')
    list_filter = ('is_primary',)
    search_fields = ('pet__name',)

# SPECIES
from .models import Species

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)

# BREED
from .models import Breed

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'id')
    list_filter = ('species',)
    search_fields = ('name',)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Shelter, Pet, Species, Breed, AdoptionRequest, Adoption


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'created_at')
    list_filter = ('role', 'is_staff')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Datos extra', {'fields': ('phone', 'role')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Datos extra', {'fields': ('email', 'phone', 'role')}),
    )


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'email', 'created_at')
    search_fields = ('name', 'address')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'shelter', 'adoption_status', 'created_at')
    list_filter = ('species', 'adoption_status', 'gender', 'size', 'shelter')
    search_fields = ('name',)


@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)


@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'id')
    list_filter = ('species',)
    search_fields = ('name',)


class AdopcionInline(admin.TabularInline):
    model = Adoption
    extra = 0


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pet', 'status', 'request_date')
    list_filter = ('status', 'request_date')
    search_fields = ('user__username', 'pet__name')
    inlines = [AdopcionInline]


@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'request', 'adoption_date')
    list_filter = ('adoption_date',)
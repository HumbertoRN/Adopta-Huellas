from django.contrib import admin
from .models import Breed, AdoptionRequest, Adoption

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name','species','id')
    list_filter = ('species',)
    search_fields = ('name',)

    class AdopcionInline(admin.TabularInline):
        model = Adoption
        extra = 0

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin)
    list_display = ('id','user','pet','status','request_date')
    list_filter = ('status','request_date')
    search_fields = ('user__username','pet__name')
    inlines = [AdopcionInline]

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ('id','request','adoption_date')
    list_filter = ('adoption_date',)
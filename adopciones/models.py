import uuid
from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# USER

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADOPTER', 'Adoptante'),
        ('SHELTER_ADMIN', 'Administrador de refugio'),
        ('ADMIN', 'Administrador'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # username y password ya vienen de AbstractUser
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='ADOPTER')
    shelter = models.ForeignKey('Shelter', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

# SHELTER

class Shelter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# PET

class Pet(models.Model):
    GENDER_CHOICES = [
        ('MALE', 'Macho'),
        ('FEMALE', 'Hembra'),
    ]
    SIZE_CHOICES = [
        ('SMALL', 'Pequeño'),
        ('MEDIUM', 'Mediano'),
        ('LARGE', 'Grande'),
    ]
    ADOPTION_STATUS_CHOICES = [
        ('AVAILABLE', 'Disponible'),
        ('IN_PROCESS', 'En proceso'),
        ('ADOPTED', 'Adoptado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shelter = models.ForeignKey('Shelter', on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.ForeignKey('Species', on_delete=models.PROTECT, related_name='pets')
    breed = models.ForeignKey('Breed', on_delete=models.SET_NULL, null=True, blank=True, related_name='pets')
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    description = models.TextField(blank=True, null=True)
    health_status = models.CharField(max_length=255, blank=True, null=True)
    adoption_status = models.CharField(max_length=20, choices=ADOPTION_STATUS_CHOICES, default='AVAILABLE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
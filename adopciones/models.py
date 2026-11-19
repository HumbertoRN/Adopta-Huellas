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

# ADOPTION_REQUEST

class AdoptionRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('APPROVED', 'Aprobado'),
        ('REJECTED', 'Rechazado'),
        ('CANCELLED', 'Cancelado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='adoption_requests')
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='adoption_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    message = models.TextField(blank=True, null=True)
    request_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Solo una solicitud aprobada por mascota
            models.UniqueConstraint(
                fields=['pet'],
                condition=Q(status='APPROVED'),
                name='unique_approved_request_per_pet',
            ),
        ]

    def __str__(self):
        return f"Solicitud de {self.user.username} por {self.pet.name} - {self.get_status_display()}"

# ADOPTION

class Adoption(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request = models.OneToOneField(
        'AdoptionRequest',
        on_delete=models.CASCADE,
        related_name='adoption',
        limit_choices_to={'status': 'APPROVED'},
    )
    adoption_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Adopción de {self.request.pet.name}"

# FAVORITE

class Favorite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'pet'], name='unique_favorite'),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.pet.name}"

# PET_IMAGE

class PetImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='pets/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Solo una imagen principal por mascota
            models.UniqueConstraint(
                fields=['pet'],
                condition=Q(is_primary=True),
                name='unique_primary_image_per_pet',
            ),
        ]

    def __str__(self):
        return f"Imagen de {self.pet.name}"

# SPECIES

class Species(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Species'

    def __str__(self):
        return self.name

# BREED

class Breed(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    species = models.ForeignKey('Species', on_delete=models.CASCADE, related_name='breeds')
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['species', 'name'], name='unique_breed_per_species'),
        ]

    def __str__(self):
        return f"{self.name} ({self.species.name})"
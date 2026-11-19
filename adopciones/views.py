from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PetForm, RegisterForm
from .models import Pet


def es_refugio(user):
    return user.role == 'SHELTER_ADMIN' and user.shelter_id is not None


# =========================
# 👤 PERSONA 1 — Cuentas
# =========================
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'adopciones/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(request,
                            username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'adopciones/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

# =========================
# CATÁLOGO
# =========================
def home(request):
    pets = Pet.objects.filter(adoption_status='AVAILABLE').order_by('-created_at')
    return render(request, 'adopciones/home.html', {'pets': pets})


# =========================
# FICHA DE MASCOTA
# =========================
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    es_favorito = (
        request.user.is_authenticated
        and Favorite.objects.filter(user=request.user, pet=pet).exists()
    )
    return render(request, 'adopciones/pet_detail.html', {'pet': pet, 'es_favorito': es_favorito})


# =========================
# SOLICITUDES DE ADOPCIÓN
# =========================
@login_required
def request_create(request, pk):
    pet = get_object_or_404(Pet, pk=pk, adoption_status='AVAILABLE')
    if request.method == 'POST':
        AdoptionRequest.objects.create(
            user=request.user,
            pet=pet,
            message=request.POST.get('message', ''),
        )
        return redirect('my_requests')
    return render(request, 'adopciones/request_form.html', {'pet': pet})


@login_required
def my_requests(request):
    solicitudes = AdoptionRequest.objects.filter(user=request.user).select_related('pet').order_by('-request_date')
    return render(request, 'adopciones/my_requests.html', {'solicitudes': solicitudes})


# =========================
# FAVORITOS
# =========================
@login_required
def favorite_list(request):
    favoritos = Favorite.objects.filter(user=request.user).select_related('pet').order_by('-created_at')
    return render(request, 'adopciones/favorite_list.html', {'favoritos': favoritos})


@login_required
def favorite_toggle(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    favorito, creado = Favorite.objects.get_or_create(user=request.user, pet=pet)
    if not creado:
        favorito.delete()
    return redirect('pet_detail', pk=pet.pk)


# =========================
# PÁGINAS
# =========================
def privacy_notice(request):
    return render(request, 'adopciones/privacy_notice.html')
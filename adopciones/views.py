from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from .forms import RegisterForm
from .models import Pet, Species
from .models import AdoptionRequest

# =========================
# 🏠 Catálogo de mascotas
# =========================
def home(request):

    query = request.GET.get('q')
    species_id = request.GET.get('species')

    pets = Pet.objects.select_related(
        'shelter', 'species', 'breed'
    ).filter(
        adoption_status='AVAILABLE'
    ).order_by('-created_at')

    # =========================
    # 🔎 Busqueda
    # =========================
    if query:
        pets = pets.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    # =========================
    # 🐾 Filtro especie
    # =========================
    if species_id:
        pets = pets.filter(
            species__id=species_id
        )

    # =========================
    # 📄 Paginacion
    # =========================
    paginator = Paginator(pets, 6)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    species = Species.objects.all()

    return render(request, 'adopciones/home.html', {
        'page_obj': page_obj,
        'species': species,
    })


# =========================
# 🐶 Detalle de mascota
# =========================
def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)

    return render(request, 'adopciones/pet_detail.html', {
        'pet': pet
    })


# =========================
# 👤 Registro
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


# =========================
# 🔑 Login
# =========================
def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(request.GET.get('next') or 'home')

        error = 'Usuario o contraseña incorrectos'

    return render(request, 'adopciones/login.html', {'error': error})


# =========================
# 🚪 Logout
# =========================
def logout_view(request):
    logout(request)
    return redirect('home')


# =========================
# 📊 Dashboard (solo refugios)
# =========================
@login_required
def dashboard(request):
    if request.user.role != 'SHELTER_ADMIN' or not request.user.shelter:
        return HttpResponseForbidden("Solo administradores de refugio")

    pets = Pet.objects.filter(
        shelter=request.user.shelter
    ).select_related('species', 'breed')

    requests = AdoptionRequest.objects.filter(
        pet__shelter=request.user.shelter
    ).select_related('user', 'pet').order_by('-request_date')

    return render(request, 'adopciones/dashboard.html', {
        'pets': pets,
        'requests': requests
    })


# =========================
# 📋 Mis solicitudes
# =========================
@login_required
def my_requests(request):
    requests = AdoptionRequest.objects.filter(
        user=request.user
    ).select_related('pet').order_by('-request_date')

    return render(request, 'adopciones/my_requests.html', {
        'requests': requests
    })
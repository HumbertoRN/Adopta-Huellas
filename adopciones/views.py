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
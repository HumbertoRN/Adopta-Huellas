from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Mascotas
    path('pets/<uuid:pk>/', views.pet_detail, name='pet_detail'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Solicitudes
    path('my-requests/', views.my_requests, name='my_requests'),
]
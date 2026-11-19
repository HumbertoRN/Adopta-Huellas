from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mascotas/<uuid:pk>/', views.pet_detail, name='pet_detail'),
    path('mascotas/<uuid:pk>/solicitar/', views.request_create, name='request_create'),
    path('mis-solicitudes/', views.my_requests, name='my_requests'),
    path('favoritos/', views.favorite_list, name='favorite_list'),
    path('favoritos/<uuid:pk>/alternar/', views.favorite_toggle, name='favorite_toggle'),
    path('aviso-de-privacidad/', views.privacy_notice, name='privacy_notice'),
    path('cuenta/registro/', views.register, name='register'),
    path('cuenta/entrar/', auth_views.LoginView.as_view(
        template_name='adopciones/login.html', redirect_authenticated_user=True), name='login'),
    path('cuenta/salir/', auth_views.LogoutView.as_view(), name='logout'),
]
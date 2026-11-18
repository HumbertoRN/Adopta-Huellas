from django.contrib.auth import views as auth_views
from django.urls import path
from .views import adopcion, catalogo, cuentas, favoritos, ficha, paginas

urlpatterns = [
    path('', catalogo.home, name='home'),                                                 
    path('mascotas/<uuid:pk>/', ficha.pet_detail, name='pet_detail'),                    
    path('mascotas/<uuid:pk>/solicitar/', adopcion.request_create, name='request_create'),  
    path('mis-solicitudes/', adopcion.my_requests, name='my_requests'),                
    path('favoritos/', favoritos.favorite_list, name='favorite_list'),                  
    path('favoritos/<uuid:pk>/alternar/', favoritos.favorite_toggle, name='favorite_toggle'), 
    path('aviso-de-privacidad/', paginas.privacy_notice, name='privacy_notice'),         
    path('cuenta/registro/', cuentas.register, name='register'),                          
    path('cuenta/entrar/', auth_views.LoginView.as_view(
        template_name='adopciones/login.html', redirect_authenticated_user=True), name='login'), 
    path('cuenta/salir/', auth_views.LogoutView.as_view(), name='logout'),            
]
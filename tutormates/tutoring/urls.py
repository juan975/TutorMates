from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path('login/', views.user_login, name='login'),
    path('', views.inicio, name="inicio"),
    path('login/',auth_views.LoginView.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.profile_view, name='perfil'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('perfil/password-change/',auth_views.PasswordChangeView.as_view(), name='password_change_form'),
    path('perfil/password-change/change_done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/',views.register, name='register'),
    path('crear_tutoria/', views.crear_tutoria, name='crear_tutoria'), 
    path('editar/<int:tutoria_id>/', views.editar_tutoria, name='editar_tutoria'),  
    path('eliminar/<int:tutoria_id>/', views.eliminar_tutoria, name='eliminar_tutoria'), 
    path('tutorias', views.listar_tutorias, name='tutorias' ),
]

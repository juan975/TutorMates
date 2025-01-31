from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Rutas generales 
    path('', views.inicio, name="inicio"),
    path('login/',auth_views.LoginView.as_view(), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.profile_view, name='perfil'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('perfil/password-change/',auth_views.PasswordChangeView.as_view(), name='password_change_form'),
    path('perfil/password-change/change_done/',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('register/',views.register, name='register'),

    # Rutas para tutores
    path('tutores/', views.listar_tutores, name='tutores'),
    path('tutores/<int:tutor_id>/', views.detalle_tutor, name='detalle_tutor'),

    # Rutas para tutorías
    path('crear_tutoria/', views.crear_tutoria, name='crear_tutoria'), 
    path('editar/<int:tutoria_id>/', views.editar_tutoria, name='editar_tutoria'),  
    path('eliminar/<int:tutoria_id>/', views.eliminar_tutoria, name='eliminar_tutoria'), 
    path('tutorias', views.listar_tutorias, name='tutorias' ),
    path('tutoria/<int:tutoria_id>/', views.detalle_tutoria, name='detalle_tutoria'),
    path('tutoria/<int:tutoria_id>/inscribirse/', views.inscribirse_tutoria, name='inscribirse_tutoria'),
    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),
    path('inscripcion/anular/<int:inscripcion_id>/', views.anular_inscripcion, name='anular_inscripcion'),

    # Rutas para administración
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/usuario/editar/<int:user_id>/', views.editar_usuario_admin, name='editar_usuario_admin'),
    path('admin/tutoria/editar/<int:tutoria_id>/', views.editar_tutoria_admin, name='editar_tutoria_admin'),
    path('admin/categoria/editar/<int:categoria_id>/', views.editar_categoria, name='editar_categoria'),
    path('admin/categoria/crear/', views.crear_categoria, name='crear_categoria'),
    path('admin/rol/crear/', views.crear_rol, name='crear_rol'),
]

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Categoria, Tutoria

class CustomUserAdmin(UserAdmin):
    # Campos que se muestran en la lista de usuarios
    list_display = ('username', 'email', 'nombre', 'apellido', 'role', 'is_staff')
    
    # Campos por los que se puede buscar
    search_fields = ('username', 'nombre', 'apellido', 'email')
    
    # Campos por los que se puede filtrar en el panel lateral
    list_filter = ('role', 'is_active', 'is_staff')
    
    # Organización de campos en el formulario de edición
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('nombre', 'apellido', 'email', 'role')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos que se muestran al crear un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'nombre', 'apellido', 'email', 'role', 'password1', 'password2'),
        }),
    )
    
    # Ordenar por username por defecto
    ordering = ('username',)

# Registrar el modelo User con la clase CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

# Agregar al administrador la clase Perfil
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['user', 'bio', 'profile_picture']
    raw_id_fields=['user']

# Agregar al administrador la clase Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

# Agregar al administrador la clase Tutoria  
@admin.register(Tutoria)
class TutoriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tutor', 'categoria', 'dia', 'hora', 'cupos')
    search_fields = ('titulo', 'categoria__nombre')
    list_filter = ('categoria', 'dia')
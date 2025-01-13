from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

#Modelo de usuario
class User(AbstractUser):
    ROLE_CHOICES = (
        ('tutor', 'Tutor'),
        ('estudiante', 'Estudiante'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='estudiante')
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_set_tutoring', 
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_set_tutoring_permissions', 
    )

#Modelo de perfil de usuario
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'
    
#Modelo de categorías
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

#Modelo de tutorías
class Tutoria(models.Model):
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutorias'
    )
    titulo = models.CharField(max_length=200)
    categoria = models.ForeignKey(
        'Categoria',
        on_delete=models.PROTECT,
        related_name='tutorias'
    )
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='tutorias/', blank=True, null=True)
    dia = models.DateField()
    hora = models.TimeField()
    cupos = models.PositiveIntegerField()

    def __str__(self):
        return self.titulo
 
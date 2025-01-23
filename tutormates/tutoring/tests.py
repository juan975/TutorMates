from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date, time
from .models import Profile, Categoria, Tutoria
from .forms import UserRegistrationForm, TutoriaForm

class UserModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.test_user = self.User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            nombre='Test',
            apellido='User',
            role='estudiante'
        )

    def test_user_creation(self):
        """Prueba la creación de un usuario y sus campos"""
        self.assertEqual(self.test_user.username, 'testuser')
        self.assertEqual(self.test_user.email, 'test@example.com')
        self.assertEqual(self.test_user.nombre, 'Test')
        self.assertEqual(self.test_user.apellido, 'User')
        self.assertEqual(self.test_user.role, 'estudiante')
        self.assertTrue(self.test_user.is_active)
        self.assertFalse(self.test_user.is_staff)

    def test_user_profile_creation(self):
        """Prueba que se crea un perfil automáticamente al crear un usuario"""
        profile = Profile.objects.get(user=self.test_user)
        self.assertIsNotNone(profile)
        self.assertEqual(str(profile), f'Perfil de {self.test_user.username}')

class CategoriaModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nombre='Matemáticas',
            descripcion='Tutorías de matemáticas básicas'
        )

    def test_categoria_creation(self):
        """Prueba la creación de una categoría"""
        self.assertEqual(str(self.categoria), 'Matemáticas')
        self.assertEqual(self.categoria.descripcion, 'Tutorías de matemáticas básicas')

class TutoriaModelTest(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.tutor = self.User.objects.create_user(
            username='tutor',
            password='tutor123',
            role='tutor'
        )
        self.categoria = Categoria.objects.create(nombre='Matemáticas')
        self.tutoria = Tutoria.objects.create(
            tutor=self.tutor,
            titulo='Álgebra básica',
            categoria=self.categoria,
            descripcion='Curso de álgebra',
            dia=date.today(),
            hora=time(14, 30),
            cupos=5
        )

    def test_tutoria_creation(self):
        """Prueba la creación de una tutoría"""
        self.assertEqual(str(self.tutoria), 'Álgebra básica')
        self.assertEqual(self.tutoria.tutor, self.tutor)
        self.assertEqual(self.tutoria.categoria, self.categoria)
        self.assertEqual(self.tutoria.cupos, 5)

class UserRegistrationFormTest(TestCase):
    def test_valid_form(self):
        """Prueba un formulario de registro válido"""
        form_data = {
            'username': 'newuser',
            'nombre': 'New',
            'apellido': 'User',
            'email': 'new@example.com',
            'role': 'estudiante',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_passwords(self):
        """Prueba que el formulario es inválido cuando las contraseñas no coinciden"""
        form_data = {
            'username': 'newuser',
            'nombre': 'New',
            'apellido': 'User',
            'email': 'new@example.com',
            'role': 'estudiante',
            'password': 'testpass123',
            'password2': 'differentpass'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class TutoriaFormTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre='Matemáticas')

    def test_valid_tutoria_form(self):
        """Prueba un formulario de tutoría válido"""
        form_data = {
            'titulo': 'Álgebra básica',
            'categoria': self.categoria.id,
            'descripcion': 'Curso de álgebra',
            'dia': '2025-01-15',
            'hora': '14:30',
            'cupos': 5
        }
        form = TutoriaForm(data=form_data)
        self.assertTrue(form.is_valid())

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        # Crear usuario estudiante
        self.estudiante = self.User.objects.create_user(
            username='estudiante',
            password='test123',
            role='estudiante'
        )
        # Crear usuario tutor
        self.tutor = self.User.objects.create_user(
            username='tutor',
            password='test123',
            role='tutor'
        )
        # Crear categoría
        self.categoria = Categoria.objects.create(nombre='Matemáticas')

    def test_inicio_view(self):
        """Prueba la vista de inicio"""
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/inicio.html')

    def test_register_view(self):
        """Prueba el registro de usuario"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_crear_tutoria_view_unauthorized(self):
        """Prueba que un estudiante no puede acceder a crear tutoría"""
        self.client.login(username='estudiante', password='test123')
        response = self.client.get(reverse('crear_tutoria'))
        self.assertNotEqual(response.status_code, 200)

    def test_crear_tutoria_view_authorized(self):
        """Prueba que un tutor puede acceder a crear tutoría"""
        self.client.login(username='tutor', password='test123')
        response = self.client.get(reverse('crear_tutoria'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutorial/create_tutorial.html')

    def test_editar_tutoria_view(self):
        """Prueba la edición de una tutoría"""
        self.client.login(username='tutor', password='test123')
        tutoria = Tutoria.objects.create(
            tutor=self.tutor,
            titulo='Test Tutoria',
            categoria=self.categoria,
            descripcion='Test',
            dia=date.today(),
            hora=time(14, 30),
            cupos=5
        )
        response = self.client.get(reverse('editar_tutoria', args=[tutoria.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutorial/edit_tutorial.html')

    def test_profile_view_protected(self):
        """Prueba que la vista de perfil requiere autenticación"""
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 302) 

    def test_profile_view_authenticated(self):
        """Prueba que un usuario autenticado puede ver su perfil"""
        self.client.login(username='estudiante', password='test123')
        response = self.client.get(reverse('perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile.html')

class TutorRequiredDecoratorTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.estudiante = self.User.objects.create_user(
            username='estudiante',
            password='test123',
            role='estudiante'
        )
        self.tutor = self.User.objects.create_user(
            username='tutor',
            password='test123',
            role='tutor'
        )

    def test_tutor_required_decorator_estudiante(self):
        """Prueba que el decorador bloquea a estudiantes"""
        self.client.login(username='estudiante', password='test123')
        response = self.client.get(reverse('crear_tutoria'))
        self.assertRedirects(response, reverse('inicio'))

    def test_tutor_required_decorator_tutor(self):
        """Prueba que el decorador permite acceso a tutores"""
        self.client.login(username='tutor', password='test123')
        response = self.client.get(reverse('crear_tutoria'))
        self.assertEqual(response.status_code, 200)
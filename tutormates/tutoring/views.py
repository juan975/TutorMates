from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserEditForm, ProfileEditForm, UserRegistrationForm, LoginForm, TutoriaForm
from .models import User, Profile, Tutoria, Role

# Verificar si el usuario es tutor
def role_required(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, "Debes iniciar sesión para acceder a esta sección.")
                return redirect('login')
            if not hasattr(request.user, 'role') or request.user.role.role_type != required_role:
                messages.error(request, "No tienes permisos para realizar esta acción.")
                return redirect('inicio')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Vista de página de inicio
def inicio(request):
    return render(request, 'account/inicio.html', {'section': 'inicio'})

# Vista de registro
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Crear el usuario
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            
            # Crear el perfil y el rol asociado
            Profile.objects.create(user=new_user)
            Role.objects.create(user=new_user, role_type=user_form.cleaned_data['role'])
            
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

# Vista del perfil
@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'account/profile.html', {
        'profile': profile,
        'role': request.user.role.get_role_type_display()
    })

# Vista para crear y mostrar tutorías del tutor registrado
@login_required
@role_required('tutor')
def crear_tutoria(request):
    if request.method == 'POST':
        form = TutoriaForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_tutoria = form.save(commit=False)
            nueva_tutoria.tutor = request.user
            nueva_tutoria.save()
            messages.success(request, "La tutoría se ha creado correctamente.")
            return redirect('crear_tutoria')
    else:
        form = TutoriaForm()
    tutorias = Tutoria.objects.filter(tutor=request.user)
    return render(request, 'tutorial/create_tutorial.html', {
        'form': form,
        'tutorias': tutorias,
    })

# Vista para editar tutorías
@login_required
@role_required('tutor')
def editar_tutoria(request, tutoria_id):
    tutoria = get_object_or_404(Tutoria, id=tutoria_id, tutor=request.user)
    if request.method == 'POST':
        form = TutoriaForm(request.POST, request.FILES, instance=tutoria)
        if form.is_valid():
            form.save()
            messages.success(request, "La tutoría se ha actualizado correctamente.")
            return redirect('crear_tutoria')
    else:
        form = TutoriaForm(instance=tutoria)
    return render(request, 'tutorial/edit_tutorial.html', {
        'form': form,
        'tutoria': tutoria,
    })

# Vista para eliminar tutorías
@login_required
@role_required('tutor')
def eliminar_tutoria(request, tutoria_id):
    tutoria = get_object_or_404(Tutoria, id=tutoria_id, tutor=request.user)
    if request.method == 'POST':
        tutoria.delete()
        messages.success(request, "La tutoría se ha eliminado correctamente.")
        return redirect('crear_tutoria')

# Vista para listar todas las tutorías
@login_required
def listar_tutorias(request):
    tutorias = Tutoria.objects.all()
    return render(request, 'tutorial/list_tutorials.html', {
        'tutorias': tutorias,
    })

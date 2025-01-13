from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserEditForm, ProfileEditForm

from .forms import UserRegistrationForm  
from .models import User, Profile, Tutoria
from .forms import LoginForm, TutoriaForm

#Verificar si el usuario es tutor
def tutor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para acceder a esta sección.")
            return redirect('login')

        if request.user.role != 'tutor':
            messages.error(request, "No tienes permisos para realizar esta acción.")
            return redirect('inicio')

        return view_func(request, *args, **kwargs)
    return _wrapped_view

#Vista de página de inicio
def inicio(request):
    return render(request, 'account/inicio.html', {'section': 'inicio'})

#Vista de página de login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User = authenticate(request, 
                                username=cd['username'], 
                                password=cd['password'])
            if User is not None:
                if User.is_active:
                    login(request, User)
                    return HttpResponse('Usuario autenticado')
                else:
                    return HttpResponse('Usuario inactivo')
            else:
                return HttpResponse('Usuario no encontrado')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

#Vista del registro
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user':new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

#Vista del perfil
@login_required
def profile_view(request):
    profile = request.user.profile 
    return render(request, 'account/profile.html', {'profile': profile})

#Vista para editar perfil
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'account/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

#Vista para crear y mostrar tutorias del tutor registrado
@login_required
@tutor_required
def crear_tutoria(request):
    if request.method == 'POST':
        form = TutoriaForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_tutoria = form.save(commit=False)
            nueva_tutoria.tutor = request.user
            nueva_tutoria.save()
            messages.success(request, "La tutoría se ha creado correctamente.")
            return redirect('crear_tutoria')  # Redirige a la misma vista después de crear.

    else:
        form = TutoriaForm()  # Muestra un formulario vacío si la solicitud es GET.

    tutorias = Tutoria.objects.filter(tutor=request.user)  # Lista de tutorías del tutor.

    return render(request, 'tutorial/create_tutorial.html', {
        'form': form,
        'tutorias': tutorias,  # Pasa las tutorías para mostrarlas en la plantilla.
    })

#Vista para editar tutorias
@login_required
@tutor_required
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

#Vista para eliminar tutoria
@login_required
@tutor_required
def eliminar_tutoria(request, tutoria_id):
    tutoria = get_object_or_404(Tutoria, id=tutoria_id, tutor=request.user)
    if request.method == 'POST':
        tutoria.delete()
        messages.success(request, "La tutoría se ha eliminado correctamente.")
        return redirect('crear_tutoria')
    
@login_required
def listar_tutorias(request):
    tutorias = Tutoria.objects.all()
    return render(request, 'tutorial/list_tutorials.html',{
        'tutorias':tutorias,
    })
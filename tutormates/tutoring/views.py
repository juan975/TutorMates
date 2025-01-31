from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .forms import UserEditForm, ProfileEditForm

from .forms import UserRegistrationForm  
from .models import Rol, User, Profile, Categoria, Tutoria, Inscripcion
from .forms import LoginForm, TutoriaForm, AdminUserEditForm, AdminTutoriaForm, AdminCategoriaForm, RolForm

#Verificar si el usuario es tutor
def tutor_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para acceder a esta sección.")
            return redirect('login')

        # Verificar si el usuario tiene el rol con id == 2 (rol tutor)
        if not request.user.rol or request.user.rol.id != 2:
            messages.error(request, "No tienes permisos para realizar esta acción.")
            return redirect('inicio')

        return view_func(request, *args, **kwargs)
    return _wrapped_view

#Verificar si el usuario es admin
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para acceder a esta sección.")
            return redirect('login')

        # Verificar si el usuario tiene el rol con id == 3 (rol amdin)
        if not request.user.rol or request.user.rol.id != 3:
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
            return render(request, 'account/register_done.html', {'new_user': new_user})
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
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect('perfil')
        else:
            messages.error(request, "Ocurrió un error al actualizar tu perfil.")
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
            return redirect('crear_tutoria')  
        else:
            messages.error(request, "Error al crear la tutoría. Verifica los datos.")
    else:
        form = TutoriaForm()  

    tutorias = Tutoria.objects.filter(tutor=request.user) 

    return render(request, 'tutorial/create_tutorial.html', {
        'form': form,
        'tutorias': tutorias,  
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
            messages.error(request, "Error al actualizar la tutoría. Verifica los datos.")
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

#Vista para ver las tutorias  
@login_required
def listar_tutorias(request):
    query = request.GET.get('q', '')  # Obtener el término de búsqueda
    categoria_id = request.GET.get('categoria', '')  # Obtener el ID de la categoría seleccionada

    # Obtener todas las tutorías
    tutorias = Tutoria.objects.all()

    # Filtrar por término de búsqueda
    if query:
        tutorias = tutorias.filter(titulo__icontains=query)

    # Filtrar por categoría si se seleccionó una
    if categoria_id:
        tutorias = tutorias.filter(categoria_id=categoria_id)

    # Obtener todas las categorías para el filtro
    categorias = Categoria.objects.all()

    return render(request, 'tutorial/list_tutorials.html', {
        'tutorias': tutorias,
        'categorias': categorias,
    })


# Detalle de una tutoría
def detalle_tutoria(request, tutoria_id):
    tutoria = get_object_or_404(Tutoria, id=tutoria_id)
    return render(request, 'tutorial/detail_tutorial.html', {'tutoria': tutoria})

# Listar todos los tutores
def listar_tutores(request):
    tutores = User.objects.filter(rol__id=2)  # Rol con ID 2 es tutor
    return render(request, 'tutors/list_tutors.html', {'tutores': tutores})

# Detalle de un tutor
def detalle_tutor(request, tutor_id):
    tutor = get_object_or_404(User, id=tutor_id, rol__id=2)  # Asegurar que es un tutor
    tutorias = Tutoria.objects.filter(tutor=tutor)  # Tutorías creadas por el tutor
    return render(request, 'tutors/detail_tutor.html', {'tutor': tutor, 'tutorias': tutorias})

# Vista de inscripción
@login_required
def inscribirse_tutoria(request, tutoria_id):
    tutoria = get_object_or_404(Tutoria, id=tutoria_id)

    # Verificar si hay cupos disponibles
    if tutoria.cupos <= tutoria.inscripciones.count():
        messages.error(request, "La tutoría no tiene cupos disponibles.")
        return redirect('detalle_tutoria', tutoria_id=tutoria.id)

    # Verificar si ya está inscrito
    if Inscripcion.objects.filter(usuario=request.user, tutoria=tutoria).exists():
        messages.info(request, "Ya estás inscrito en esta tutoría.")
        return redirect('detalle_tutoria', tutoria_id=tutoria.id)

    # Crear la inscripción
    if request.method == 'POST':
        Inscripcion.objects.create(usuario=request.user, tutoria=tutoria)
        messages.success(request, "Inscripción realizada con éxito.")
        return redirect('detalle_tutoria', tutoria_id=tutoria.id)

    return render(request, 'tutorial/register_tutorial.html', {'tutoria': tutoria})

# Vista de mis inscripciones
@login_required
def mis_inscripciones(request):
    inscripciones = request.user.inscripciones.all()  # Inscripciones del usuario
    return render(request, 'tutorial/my_registrations.html', {'inscripciones': inscripciones})

@login_required
def anular_inscripcion(request, inscripcion_id):
    # Obtener la inscripción correspondiente
    inscripcion = get_object_or_404(Inscripcion, id=inscripcion_id, usuario=request.user)

    # Eliminar la inscripción
    if request.method == 'POST':
        inscripcion.delete()
        messages.success(request, "Tu inscripción ha sido anulada correctamente.")
        return redirect('mis_inscripciones')

    # En caso de acceder mediante GET, redirigir a la lista de inscripciones
    messages.error(request, "No se pudo anular la inscripción.")
    return redirect('mis_inscripciones')


# VISTAS ADMINISTRADOR

@login_required
@admin_required
def admin_dashboard(request):
    usuarios = User.objects.all()
    categorias = Categoria.objects.all()
    roles = Rol.objects.all()
    tutorias = Tutoria.objects.all()

    # Número de elementos por página
    items_per_page = 15  

    # Función para paginar cualquier queryset
    def paginate_queryset(queryset, page_number):
        paginator = Paginator(queryset, items_per_page)
        return paginator.get_page(page_number)

    # Obtener páginas paginadas
    usuarios_page = paginate_queryset(usuarios, request.GET.get('page_usuarios', 1))
    tutorias_page = paginate_queryset(tutorias, request.GET.get('page_tutorias', 1))
    categorias_page = paginate_queryset(categorias, request.GET.get('page_categorias', 1))
    roles_page = paginate_queryset(roles, request.GET.get('page_roles', 1))

    context = {
        'usuarios': usuarios_page,
        'categorias': categorias_page,
        'roles': roles_page,
        'tutorias': tutorias_page,
    }

    return render(request, 'admin/admin_dashboard.html', context)

# Vist para editar usuarios
@login_required
@admin_required
def editar_usuario_admin(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Error al actualizar el usuario.")
    else:
        form = AdminUserEditForm(instance=usuario)  # Aquí el formulario correcto
    return render(request, 'admin/edit_user.html', {'form': form, 'usuario': usuario})

# Vista para editar tutoria
@login_required
@admin_required
def editar_tutoria_admin(request, tutoria_id):
    tutoria = get_object_or_404(Tutoria, id=tutoria_id)
    if request.method == 'POST':
        form = AdminTutoriaForm(request.POST, request.FILES, instance=tutoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Tutoría actualizada correctamente.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Error al actualizar la tutoría.")
    else:
        form = AdminTutoriaForm(instance=tutoria)
    return render(request, 'admin/edit_tutorial.html', {'form': form, 'tutoria': tutoria})

# Vista para editar categoria
@login_required
@admin_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    if request.method == 'POST':
        form = AdminCategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada correctamente.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Error al actualizar la categoría.")
    else:
        form = AdminCategoriaForm(instance=categoria)
    return render(request, 'admin/edit_categori.html', {'form': form, 'categoria': categoria})

#Vista para crear categoria
@login_required
@admin_required
def crear_categoria(request):
    if request.method == 'POST':
        form = AdminCategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada correctamente.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Error al crear la categoría.")
    else:
        form = AdminCategoriaForm()
    return render(request, 'admin/create_categori.html', {'form': form})

#Vista para crear rol
@login_required
@admin_required
def crear_rol(request):
    if request.method == 'POST':
        form = RolForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol creado correctamente.")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Error al crear el rol.")
    else:
        form = RolForm()
    return render(request, 'admin/create_role.html', {'form': form})

# Vista de Admin con Sidebar
@login_required
@admin_required
def admin_dashboard(request):
    section = request.GET.get('section', 'usuarios')  # Por defecto, muestra "Usuarios"

    context = {
        'usuarios': User.objects.all(),
        'categorias': Categoria.objects.all(),
        'roles': Rol.objects.all(),
        'tutorias': Tutoria.objects.all(),
        'section': section,  # Enviar la sección seleccionada
    }
    
    return render(request, 'admin/admin_dashboard.html', context)

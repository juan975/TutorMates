from django import forms 
from .models import Rol, User, Profile, Categoria, Tutoria

# Formulario de Login
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# Formulario de registro de usuairos
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput)
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.filter(visible=True), #Filtrar lo roles que son visibles
        label="Rol",
        empty_label="Seleccione un rol"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'rol']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

# Formulario para editar los usuarios  
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Formulario para editar el perfil del usuario
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

# Formulario para las tutorias
class TutoriaForm(forms.ModelForm):
    class Meta:
        model = Tutoria
        fields = ['titulo', 'categoria', 'descripcion', 'imagen', 'dia', 'hora', 'cupos']
        widgets = {
            'dia': forms.SelectDateWidget,
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

# FORMULARIOS DE ADMINISTRADOR

# Editar usuario
class AdminUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'rol', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].queryset = Rol.objects.all()

# Editar tutorias
class AdminTutoriaForm(forms.ModelForm):
    class Meta:
        model = Tutoria
        fields = ['titulo', 'descripcion', 'imagen', 'dia', 'hora', 'cupos', 'categoria']
        widgets = {
            'dia': forms.SelectDateWidget,
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

# Editar categorias
class AdminCategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']

# Editar roles

class RolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ['rol', 'descripcion', 'visible']

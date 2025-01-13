from django import forms 
from .models import User, Profile, Tutoria

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repite la contraseña', widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label="Rol")

    class Meta:
        model = User
        fields = ['username', 'nombre', 'apellido', 'email', 'role']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

class TutoriaForm(forms.ModelForm):
    class Meta:
        model = Tutoria
        fields = ['titulo', 'categoria', 'descripcion', 'imagen', 'dia', 'hora', 'cupos']
        widgets = {
            'dia': forms.SelectDateWidget,
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from datetime import datetime,timedelta
GENERO_CHOICES=[('M','Masculino'),('F','Femenino'),('X','Otro'),]
NOMBRE_DIA=('Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo')
ciudades=[]
especialidades=[]
CIUDADES_CHOICES=[]
ESPECIALIDADES_CHOICES=[]

doctores = Doctor.objects.all()
for doctor in doctores:
    ciudades.append(doctor.city)
    especialidades.append(doctor.specialty)
ciudades=list(set(ciudades))
ciudades.sort()
for i in range(len(ciudades)):
    CIUDADES_CHOICES.append((ciudades[i],ciudades[i]))
especialidades=list(set(especialidades))
especialidades.sort()
for i in range(len(especialidades)):
    ESPECIALIDADES_CHOICES.append((especialidades[i],especialidades[i]))


class LoginForm(forms.Form):
    mail=forms.EmailField(label = "Correo electronico",max_length=255, required=True)
    password=forms.CharField(widget=forms.PasswordInput(),label = "Contraseña",max_length=255, required=True)

class SignupPacienteForm(forms.Form):
    firstname=forms.CharField(label = "Nombre",max_length=255, required=True)
    lastname=forms.CharField(label = "Apellido",max_length=255, required=True)
    password=forms.CharField(widget=forms.PasswordInput(),label = "Contraseña",max_length=255, required=True)
    passwordRepeat=forms.CharField(widget=forms.PasswordInput(),label = "Repita su contraseña",max_length=255, required=True)
    mail=forms.EmailField(label = "Correo electronico",max_length=255, required=True)
    phone=forms.IntegerField(label = "Telefono (Ejemplo: 9XXXXXXXX)",max_value=999999999,min_value=111111111,required=True)
    address=forms.CharField(label = "Direccion",max_length=255, required=False)

    firstname.widget.attrs.update({'placeholder': 'Juan'})
    lastname.widget.attrs.update({'placeholder': 'Perez'})
    password.widget.attrs.update({'placeholder': '******'})
    passwordRepeat.widget.attrs.update({'placeholder': '******'})
    mail.widget.attrs.update({'placeholder': 'juan@gmail.com'})
    phone.widget.attrs.update({'placeholder': '912345678'})
    address.widget.attrs.update({'placeholder': 'Avenue #123'})

class AddDoctorForm(forms.Form):
    person_id=forms.IntegerField(label = "Numero ID",max_value=100000000,min_value=0, required=True)
    first_name=forms.CharField(label = "Nombre",max_length=255, required=True)
    last_name=forms.CharField(label = "Apellido",max_length=255, required=True)
    gender=forms.ChoiceField(label = "Sexo",choices=GENERO_CHOICES, required=True)
    address1=forms.CharField(label = "Direccion",max_length=255, required=True)
    city=forms.ChoiceField(label = "Ciudad",choices=CIUDADES_CHOICES, required=True)
    phone=forms.IntegerField(label = "Telefono (Ejemplo: 9XXXXXXXX)",max_value=999999999,min_value=111111111,required=True)
    sub_specialty=forms.ChoiceField(label = "Especialidad",choices=ESPECIALIDADES_CHOICES, required=True)

    person_id.widget.attrs.update({'placeholder': '123456789'})
    first_name.widget.attrs.update({'placeholder': 'Juan'})
    last_name.widget.attrs.update({'placeholder': 'Perez'})
    phone.widget.attrs.update({'placeholder': '912345678'})
    address1.widget.attrs.update({'placeholder': 'Avenue #123'})


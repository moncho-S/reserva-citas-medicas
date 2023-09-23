from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Doctor(models.Model):
    person_id = models.CharField(max_length=255, blank=True, null=True) 
    first_name = models.CharField(max_length=255, blank=True, null=True) 
    last_name = models.CharField(max_length=255, blank=True, null=True) 
    gender = models.CharField(max_length=255, blank=True, null=True) 
    city = models.CharField(max_length=255, blank=True, null=True)  
    address = models.CharField(max_length=255, blank=True, null=True)  
    state = models.CharField(max_length=255, blank=True, null=True) 
    phone = models.CharField(max_length=255, blank=True, null=True)  
    specialty = models.CharField( max_length=255, blank=True, null=True) 
    active = models.BooleanField(default=True, blank=True, null=True)
    
    def __str__(self):
        fullname=self.first_name+" "+self.last_name
        return fullname

class Paciente(models.Model):
    """Modelo complementario creado para
    guardar mas atributos correspondientes a
    los pacientes creados con la clase User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

class Reserva(models.Model):
    """cada hora reservada tiene un usuario y un doctor
    asociado, junto a una variable 'done' que se marca como pendiente
    o terminada si la consulta se realizó o no"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    done= models.BooleanField(default=False)



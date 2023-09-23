from django.contrib import admin
from .models import *
#Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display =['id',
                    'person_id',
                    'first_name',
                    'last_name',
                    'gender',
                    'specialty',
                    'active'
                    ]
class PacienteAdmin(admin.ModelAdmin):
    list_display =['user',
                    'phone',
                    'address'
                    ]
class ReservaAdmin(admin.ModelAdmin):
    list_display =['user',
                    'doctor',
                    'date',
                    'done'
                    ]
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Paciente,PacienteAdmin)
admin.site.register(Reserva,ReservaAdmin)
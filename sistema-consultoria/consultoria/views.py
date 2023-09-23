from django.shortcuts import render
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
import django.contrib.auth
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .forms import *
from datetime import datetime
# Create your views here.

from sqids import Sqids
sqids = Sqids(min_length=11,alphabet="FxnXM1kBhsAvjW3Co7l2RePyY8DwaU04TIJOgb5ZE")
def codificarId(id):
    idCoded = sqids.encode([id])
    return idCoded#str
def decodificarId(id):
    idDecoded = sqids.decode(id)
    return idDecoded[0]#int

def validarRut(rut):
    try:
        numero = rut[:-1]
        verificador = rut[-1]
        if verificador=='k':
            verificador = 'K'
        iterador = 2  # multiplicador de 2 a 7
        suma = 0
        for i in range(0, len(numero)):
            r = int(numero[len(numero)-i-1])*iterador
            suma += r
            iterador = iterador+1
            if iterador == 8:
                iterador = 2
        resto = suma % 11
        dv = 11-resto
        if dv == 10:
            dv='K'
            #print("DV: K")
        elif dv == 11:
            dv='0'
            #print("DV: 0")
        else:
            dv=str(dv)
            #print("DV: ", dv)
        if verificador==dv:
            return True
        return False
    except:
        return False
    return False


DIAS_FERIADOS=[
    datetime(2010,1,1),#1 de enero
    datetime(2010,5,1),#dia del trabajador
    datetime(2010,9,18),#fiestas patrias
    datetime(2010,9,19),#glorias del ejercito
    datetime(2010,12,25)#navidad
]
DIAS=28#DIAS habiles siguientes
DURACION_VISITA=30#minutos
PRIMER_DIA_HABIL_SEMANA=0#0:LUNES,1:MARTES,2:MIERCOLES,3:JUEVES,4:VIERNES,5:SABADO,6:DOMINGO
ULTIMO_DIA_HABIL_SEMANA=4#0:LUNES,1:MARTES,2:MIERCOLES,3:JUEVES,4:VIERNES,5:SABADO,6:DOMINGO
PRIMERA_HORA_DIA=(8,8,8,8,10)#lunes a viernes
ULTIMA_HORA_DIA=(19,19,19,19,12)#lunes a viernes
EXISTE_ALMUERZO=True
INICIO_HORA_ALMUERZO=12
TERMINO_HORA_ALMUERZO=15
GENERO_CHOICES=[('M','Masculino'),('F','Femenino'),('X','Otro'),]
NOMBRE_DIA=('Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo')

ciudades=[]
especialidades=[]
CIUDADES_CHOICES=[]
ESPECIALIDADES_CHOICES=[]

def refrescarListas():
    """se refrescan las listas desplegables de ciudades y doctores
    para filtrar los resultados requeridos por el usuario"""
    global ciudades
    global especialidades
    global CIUDADES_CHOICES
    global ESPECIALIDADES_CHOICES
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

refrescarListas()

def getDiaNombre(anno,mes,dia):
        diaSemana=datetime(anno,mes,dia).weekday()
        return diaSemana,NOMBRE_DIA[diaSemana]
    
def verificarDiaFeriado(mes,dia):
    for i in range(len(DIAS_FERIADOS)):
        if DIAS_FERIADOS[i].month==mes and DIAS_FERIADOS[i].day==dia:
            return True
    return False

def usernameExists(username):
    if User.objects.filter(username=username).exists():
        return True
    return False

def doctorExists(rut):
    if Doctor.objects.filter(person_id=rut).exists():
        return True
    return False



def deleteReservasView(request,id):
    id=decodificarId(id)
    Reserva.objects.filter(id=id).delete()
    messages.success(request,f'Cita eliminada con exito!')
    context={}
    return HttpResponseRedirect("../")
    #return render(request,'reservar.html',context)

def howToView(request):
    context={}
    return render(request,'howto.html',context)

def confirmReservasView(request,id):
    id=decodificarId(id)
    Reserva.objects.filter(id=id).update(done=True)
    messages.success(request,f'Cita confirmada con exito!')
    context={}
    return HttpResponseRedirect("../")
    #return render(request,'reservar.html',context)

def misReservasView(request):
    reservas=0
    pacientes=''
    if request.method =='POST':
        paciente=request.POST['pacienteInput']
        doctor=request.POST['doctorInput']
        verCitas=request.POST['citasInput']
        verCitas=request.POST['citasInput']

        if paciente!='Usuario del paciente' and doctor!='Doctor' and verCitas=='todas':
            paciente=int(paciente)
            doctor=int(doctor)
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(user__id=paciente,doctor__id=doctor).order_by('-date')
        elif paciente!='Usuario del paciente' and doctor!='Doctor' and verCitas=='pendientes':
            paciente=int(paciente)
            doctor=int(doctor)
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(user__id=paciente,doctor__id=doctor,done=False).order_by('-date')
        elif paciente!='Usuario del paciente' and doctor!='Doctor' and verCitas=='terminadas':
            paciente=int(paciente)
            doctor=int(doctor)
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(user__id=paciente,doctor__id=doctor,done=True).order_by('-date')

        elif paciente!='Usuario del paciente' and verCitas=='todas':
            paciente=int(paciente)
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(user__id=paciente).order_by('-date')
        elif paciente!='Usuario del paciente' and verCitas=='pendientes':
            paciente=int(paciente)
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(user__id=paciente,done=False).order_by('-date')
        elif paciente!='Usuario del paciente' and verCitas=='terminadas':
            paciente=int(paciente)
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(user__id=paciente,done=True).order_by('-date')

        elif doctor!='Doctor' and verCitas=='todas':
            doctor=int(doctor)
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(doctor__id=doctor).order_by('-date')
        elif doctor!='Doctor' and verCitas=='pendientes':
            doctor=int(doctor)
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(doctor__id=doctor,done=False).order_by('-date')
        elif doctor!='Doctor' and verCitas=='terminadas':
            doctor=int(doctor)
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(doctor__id=doctor,done=True).order_by('-date')

        elif verCitas=='todas':
            reservas = Reserva.objects.select_related('user').select_related('doctor').all().order_by('-date')
        elif verCitas=='pendientes':
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(done=False).order_by('-date')
        elif verCitas=='terminadas':
            reservas = Reserva.objects.select_related('user').select_related('doctor').filter(done=True).order_by('-date')
        else:
            reservas = Reserva.objects.select_related('user').select_related('doctor').all().order_by('-date')
            
    else:
        if request.user.is_superuser:
            reservas=Reserva.objects.select_related('user').select_related('doctor').all().order_by('-date')
        
        elif request.user.is_authenticated:#para los pacientes
            reservas=Reserva.objects.select_related('user').select_related('doctor').filter(user__username=request.user.username).order_by('-date')
        
    if request.user.is_authenticated:
        try:
            for r in reservas:
                r.id_hidden = codificarId(r.id)
                r.dateStr=r.date.strftime("%d/%b/%Y %H:%M")
                if r.done==False:
                    r.estado='Pendiente'
                else:
                    r.estado='Terminada'
        except:
            pass
        #paciente y doctores para la vista del admin
        pacientes=Paciente.objects.select_related('user').all().order_by('user__username')
        doctores=Doctor.objects.all().order_by('first_name')
        context={
        'reservas':reservas,  
        'pacientes':pacientes, 
        'doctores':doctores, 
            }
    return render(request,'misreservas.html',context)

def listadoView(request):
    
    if request.method=="POST":
        id=request.POST['idInput']
        especialidad=request.POST['especialidadInput']
        city=request.POST['cityInput']
        gender=request.POST['genderInput']
        try:
            if id!='': 
                data = Doctor.objects.filter(person_id=id)
            elif especialidad!='Especialidad' and gender!='Genero' and city!='Ciudad':
                data = Doctor.objects.filter(specialty=especialidad,gender=gender,city=city,active=True)

            elif especialidad!='Especialidad' and city!='Ciudad':
                data = Doctor.objects.filter(specialty=especialidad,city=city,active=True)

            elif especialidad!='Especialidad' and gender!='Genero':
                data = Doctor.objects.filter(specialty=especialidad,gender=gender,active=True)

            elif city!='Ciudad' and gender!='Genero':
                data = Doctor.objects.filter(city=city,gender=gender,active=True)

            elif especialidad!='Especialidad':
                data = Doctor.objects.filter(specialty=especialidad,active=True)
            elif gender!='Genero':
                data = Doctor.objects.filter(gender=gender,active=True)
            elif city!='Ciudad':
                data = Doctor.objects.filter(city=city,active=True)
            else:
                data=Doctor.objects.filter(active=True)

        except:
            print('exception')
            data=''
    else:
        data=Doctor.objects.filter(active=True)

    for d in data:
        d.id_hidden = codificarId(d.id)

    refrescarListas()
    context={
        'data':data,
        'especialidades':especialidades,    
        'ciudades':ciudades,    
        'especialidades':especialidades,    
            }
    return render(request,'listado.html',context)

def reservarView(request,id):
    error=0
    doctor=0
    form=0
    id=decodificarId(id)
    doctor=Doctor.objects.filter(id=id)[0]#se toma el doctor mediante id
    print('doctor',doctor)
    if request.method=='POST':
        #form = ReservarForm(request.POST)
        #if form.is_valid():
        comentario = request.POST["comment"]
        fechaReservaStr = request.POST["fecha"]
        #comentario = form.cleaned_data["comment"]
        #fechaReservaStr = form.cleaned_data["fecha"]
        year,month,day,hours,minutes=fechaReservaStr.split(',')
        year=int(year)
        month=int(month)
        day=int(day)
        hours=int(hours)
        minutes=int(minutes)
        if minutes==0 or minutes==30:
            fechaReservaDateTime=datetime(year,month,day,hours,minutes)
            reservaActualesDoctor=Reserva.objects.select_related('doctor').filter(doctor__id=doctor.id)
            #verificar que la fecha reservada sea una inexistente abtes de guardarla en las reservas
            #   en caso que el usuario modifique el html para escoger una fecha ya ocupada        
            reservaValida=True
            try:
                for r in reservaActualesDoctor:
                    year=r.date.year
                    month=r.date.month
                    day=r.date.day
                    hours=r.date.hour
                    minutes=r.date.minute
                    reservaIteracion=datetime(year,month,day,hours,minutes)
                    if reservaIteracion==fechaReservaDateTime:
                        reservaValida=False
                        break
                    reservaValida=True
            except:
                print('se dispara la excepcion')
            if reservaValida==True:
                reserva=Reserva(user=request.user, 
                                doctor=doctor, 
                                comment=comentario,
                                date=fechaReservaDateTime)
                reserva.save()
                messages.success(request,f'Hora agendada con exito con el doctor {doctor.first_name} {doctor.last_name} a las {str(hours)}:{(str(minutes)).zfill(2)} el dia {str(day)}/{(str(month)).zfill(2)}/{str(year)} para {request.user.first_name}  {request.user.last_name}!')
                return HttpResponseRedirect("../")
            else:
                messages.error(request,f'La hora seleccionada ya se encuentra ocupada, por favor, escoja otra fecha!')
                return HttpResponseRedirect("../")
        else:
                messages.error(request,f'Por favor, escoja otra fecha!')
                return HttpResponseRedirect("../")
    else:
        if request.user.is_authenticated==True:
            reservaActualesDoctor=Reserva.objects.select_related('doctor').filter(doctor__id=doctor.id,done=False)
            dateInicial=datetime.now()+timedelta(days=2)
            dateInicial=datetime(dateInicial.year,dateInicial.month,dateInicial.day)
            fechasDisponibles=[]

            for dia in range(0,DIAS+1):
                dateIteracion=dateInicial+timedelta(days=dia)
                diaSemanaNumero,diaSemanaNombre=getDiaNombre(dateIteracion.year,dateIteracion.month,dateIteracion.day)
                if diaSemanaNumero>=PRIMER_DIA_HABIL_SEMANA and diaSemanaNumero<=ULTIMO_DIA_HABIL_SEMANA:
                    verify=verificarDiaFeriado(dateIteracion.month,dateIteracion.day)
                    if verify==False:
                        for horaIteracion in range(PRIMERA_HORA_DIA[diaSemanaNumero],ULTIMA_HORA_DIA[diaSemanaNumero]+1):
                            if EXISTE_ALMUERZO==True and horaIteracion>=INICIO_HORA_ALMUERZO and horaIteracion<TERMINO_HORA_ALMUERZO:
                                continue#se salta las horas de colacion
                            for minutoIteracion in range(0,60,DURACION_VISITA):#de 0 a 60 en intervalos de 30
                                fecha=datetime(dateIteracion.year,dateIteracion.month,dateIteracion.day,horaIteracion,minutoIteracion)
                                fechaValue=fecha.strftime("%Y,%m,%d,%H,%M")   
                                fechaVista=diaSemanaNombre+" "+fecha.strftime("%d/%b/%Y %H:%M")
                                fechasDisponibles.append((fechaValue,fechaVista,fecha))
            for r in reservaActualesDoctor:
                r.dateInTime=datetime(r.date.year,r.date.month,r.date.day,r.date.hour,r.date.minute)
                for fd in fechasDisponibles:
                    if r.dateInTime==fd[2]:
                        fechasDisponibles.remove(fd)
                        break
    context={'error':error,
                'fechasDisponibles':fechasDisponibles,
                'doctor':doctor,
                }

    return render(request,'reservar.html',context)
    
def agregarView(request):
    global ciudades
    global especialidades
    global CIUDADES_CHOICES
    global ESPECIALIDADES_CHOICES
    error=0
    form=0
    if request.method=='POST':
        #form = AddDoctorForm(request.POST)
        #if form.is_valid():
        #personID = form.cleaned_data["person_id"]
        personID = request.POST["person_id"]
        validacionRut=validarRut(personID)
        nombre = request.POST["first_name"]
        apellido = request.POST["last_name"]
        genero = request.POST["gender"]
        ciudad = request.POST["city"]
        direccion = request.POST["address1"]
        telefono = request.POST["phone"]
        telefono=str(telefono)
        rutExiste=doctorExists(personID)
        if len(telefono)==9:
            validacionTelefono=True
        else:
            validacionTelefono=False
        telefonoStr = "+56"+str(telefono)
        especialidad = request.POST["specialty"]
        
        if validacionRut==True:
            if rutExiste==False:
                if validacionTelefono==True:
                    doctor=Doctor(person_id=personID, 
                                    first_name=nombre, 
                                    last_name=apellido, 
                                    gender=genero, 
                                    address=direccion, 
                                    city=ciudad, 
                                    phone=telefonoStr, 
                                    specialty=especialidad
                                    )
                    doctor.save() 
                    messages.success(request,f'{nombre} ha sido agregado exitosamente!')
                    return HttpResponseRedirect("../")
                else:
                    error='telefono invalido'
            else: 
                error='rut registrado'
        else:
            error='rut invalido'
    else:
        form=AddDoctorForm()
    refrescarListas()
    context={'error':error,
             'form':form,
             'especialidades':especialidades,    
            'ciudades':ciudades,                
             }
    return render(request,'agregar.html',context)






def loginView(request):
    error=0
    form=''
    if request.method=='POST':
        #form = LoginForm(request.POST)
        #if form.is_valid():
        correo=request.POST['mail']
        contrasena=request.POST['password']

        #correo = form.cleaned_data["mail"]
        #contrasena = form.cleaned_data["password"]
        verify=usernameExists(correo)
        if verify==True:
            user= authenticate(username=correo,password=contrasena)
            if user is not None:
                row=User.objects.filter(username=correo)
                nombre=row[0].first_name
                login(request,user)
                messages.info(request,f'Bienvenido {nombre}!')
                return HttpResponseRedirect("../")
            else:
                error='contraseña incorrecta'
        else:
            error='correo inexistente'
            
        
    else:
        form = LoginForm()
    context={'error':error,
                'form':form}
    return render(request,'login.html',context)

def logoutView(request):
    logout(request)
    messages.info(request,"Se ha cerrado la sesion")
    return HttpResponseRedirect("../")

def signupPacienteView(request):
    error=0
    form=''
    if request.method=='POST':
        #form = SignupPacienteForm(request.POST)
        #if form.is_valid():
        #nombre=form.cleaned_data['firstname']
        nombre=request.POST['firstname']
        apellido=request.POST['lastname']
        usuario=request.POST['mail']
        correo=request.POST['mail']
        contrasena=request.POST['password']
        contrasenaRepetida=request.POST['passwordRepeat']
        direccion=request.POST['address']
        telefono=request.POST['phone']
        if len(telefono)==9:
            validacionTelefono=True
        else:
            validacionTelefono=False
        telefonoStr = "+56"+str(telefono)
        if validacionTelefono==True:
            if contrasena==contrasenaRepetida:
                verify=usernameExists(usuario)
                if verify==False:
                    user = User.objects.create_user(username=usuario, password=contrasena,first_name=nombre,last_name=apellido,email=correo)    
                    u = User.objects.get(username=usuario)
                    paciente=Paciente(user=u, phone=telefonoStr, address=direccion)
                    paciente.save()
                    user = authenticate(username=usuario,password=contrasena)
                    if user is not None:
                        login(request,user)
                        messages.info(request,f'Bienvenido {nombre}!')
                        return HttpResponseRedirect("../")
                else:
                    error='correo existente'
            else:
                error='contrasena no es igual'
        else:
            error='telefono invalido'

    else:
        form=SignupPacienteForm()
    context={'error':error,
             'form':form,
             }
    return render(request,'signup.html',context)
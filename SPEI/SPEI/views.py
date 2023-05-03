# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de tiempo
import datetime

# Librería para sha512
import hashlib

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql

# ***** Login *****
def spei(request):
    # *** Plantilla ***
    return render(request, 'index.html', context={})
# ***** Fin Login *****

# ***** Main *****
def main(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()
        
        # Se traen los valores del formulario
        user = request.POST['txtUser']
        password = request.POST['txtPassword']
        
        # Se convierte el password a sha512
        password = hashlib.sha512( str( password ).encode("utf-8") ).hexdigest()

        # Se consulta si existe el usuario en la Base de Datos 
        select = (""" SELECT count(*) 
                      FROM inginious.users 
                      WHERE username = %s AND password = %s """)
        parametros = (user,password)
        cursor.execute(select, parametros)
        user_counter = cursor.fetchone()

        # Si contador es mayor a 0, el usuario existe en la Base de Datos
        if user_counter[0] > 0 :

            # Se consultan los profesores para los cursos
            cursor.execute(""" SELECT tutors 
                               FROM inginious.aggregations
                               WHERE courseid IN('FDP-2022-1', 'FDP-2022-2',
                               'FDP-01-2023-1','FPOO-Victor-2023-1') """)
            record = cursor.fetchall()

            # Se extraen los elementos del cursos
            teacher = str(record)
            teacher = teacher.replace("[(['","")
            teacher = teacher.replace("],)]","")
            teacher = teacher.replace("'","")
            teacher = teacher.replace(" ","")
            teacher = teacher.split(",")
            
            # Se define la variable contador para cargar el dashboard del profesor o estudiante
            contador_profesor = 0

            # Se recorren los elementos del vector
            for row in teacher:
                # Si el nombre de usuario es igual al del vector 
                if (user == row):
                    # Se incrementa el contador del profesor
                    contador_profesor = 1
                    # Se carga el curso correspondiente

            # Si contador es igual a 1 el usuario es un profesor
            if contador_profesor == 1:
                # *** Dashboard Profesor ***
                # Se cargan las variables de sesión
                request.session['user'] = user
                request.session['role'] = 'Profesor'

                # Se cargan las variables de sesión al contexto
                context = {"user": request.session['user'], 
                           "role": request.session['role']}

                # Se renderiza con el Contexto con los parámetros
                return render(request, 'teacher_template.html', context= context)

            # Sino el usuario es un estudiante
            else:
                # *** Dashboard Estudiante ***
                # Se cargan las variables de sesión
                request.session['user'] = user
                request.session['role'] = 'Estudiante'

                # Se cargan las variables de sesión al contexto
                context = {"user": request.session['user'], 
                           "role": request.session['role']}
                
                # Se renderiza con el Contexto con los parámetros
                return render(request, 'student_template.html', context= context)
 
        # Sino el usuario no existe en la Base de Datos
        else:
            message = "Nombre de usuario o contraseña incorrectos."
            context = {"return": message}
            # *** Plantilla ***
            return render(request, 'index.html', context= context)
        
        # ***** Fin validación de usuarios *****

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Main *****


# ***** Student Dashboard*****
def student_dashboard(request):
    # Validación de variables de sesión
    try:
        # Se cargan las variables de sesión al contexto
        context = {"user": request.session['user'], 
                   "role": request.session['role']}
        
        # Se renderiza con el Contexto con los parámetros
        return render(request, 'student_template.html', context= context)
    
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Student Dashboard *****




# ***** Teacher Dashboard*****
def teacher_dashboard(request):
    # Validación de variables de sesión
    try:
        # Se cargan las variables de sesión al contexto
        context = {"user": request.session['user'], 
                   "role": request.session['role']}
        
        # Se renderiza con el Contexto con los parámetros
        return render(request, 'teacher_template.html', context= context)
    
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Teacher Dashboard *****



# ***** Cerrar sesión *****
def sign_off(request):
    # Se eliminan las variables de sesión
    del request.session['user']
    del request.session['role']

    # *** Plantilla ***
    return render(request, 'index.html', context={})
# ***** Fin cerrar sesión *****


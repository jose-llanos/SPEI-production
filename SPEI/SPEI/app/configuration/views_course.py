# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de fecha
from datetime import date, datetime

# Se importa la librería para envío de correos
from django.core.mail import EmailMessage

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql


# ***** Cursos  *****
def list_course(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se consultan los cursos
        cursor.execute("""  SELECT * 
                            FROM early_intervention.courses """)
        record = cursor.fetchall()

        context = {"record": record,
                   "user":   request.session['user'], 
                   "role":   request.session['role']}
        
        # *** Plantilla ***
        return render(request, 'configuration/list_course.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Cursos *****



# ***** Nuevo Curso *****
def new_course(request):
    # Validación de variables de sesión
    try:
        context = {"user":   request.session['user'], 
                   "role":   request.session['role']}
        # *** Plantilla ***
        return render(request, 'configuration/new_course.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Nuevo Curso *****



# ***** Modificar/Guardar Curso *****
def save_course(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        id = request.POST['txtId']
        txtCourseName = request.POST['txtCourseName']
        txtAcronym = request.POST['txtAcronym']
        cmbState = request.POST['cmbState']

        ### Modificar ###
        # Si el registro existe se actualiza
        if id != "":
            # Se modifica el registro en la tabla: intervention_message
            update = """ UPDATE early_intervention.courses 
                         SET course_name = %s,
                         course_acronym = %s,
                         state = %s
                         WHERE id = %s """
            parameter = (txtCourseName, 
                         txtAcronym,
                         cmbState, 
                         id)
            cursor.execute(update, parameter)

        ### Guardar ###
        # Si no existe el registro se inserta el registro en la tabla
        elif id == "":
            # Se guarda el registro en la tabla
            insert = (""" INSERT INTO early_intervention.courses 
                          (course_name, course_acronym, state)
                          VALUES(%s, %s, %s) """)
            parameter = (txtCourseName, 
                         txtAcronym, 
                         cmbState)
            cursor.execute(insert, parameter)

        # *** Plantilla ***
        return list_course(request)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Modificar/Guardar Curso  *****



# ***** Operación Curso *****
def operation_course(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        operation = request.POST['idOperation']
        operation = operation.replace(" ","")
        operation = operation.split("-")

        ### Modificar ###
        # Si el botón opción es modificar
        if operation[0] == "update":
            # Se trae el id a modificar
            id = operation[1]

            # Se consulta el curso
            select = (""" SELECT course_name, course_acronym, state
                          FROM early_intervention.courses
                          WHERE id = %(id)s """)
            cursor.execute(select, {'id': id})
            record = cursor.fetchall()

            for row in record:
                course_name = str(row[0])
                acronym = str(row[1])
                state = str(row[2])

            context = {"id":           id,
                       "course_name":  course_name, 
                       "acronym":      acronym, 
                       "state":        state,
                       "user":         request.session['user'], 
                       "role":         request.session['role']}
        
            # *** Plantilla ***
            return render(request, 'configuration/new_course.html', context= context)

        ### Eliminar ###
        # Si el botón opción es eliminar
        elif operation[0] == "delete":
            
            id = operation[1]

            # Se elimina el registro de la tabla
            delete = (""" DELETE FROM early_intervention.courses 
                          WHERE id = %(id)s """)
            cursor.execute(delete, {'id': id})

            # *** Plantilla ***
            return list_course(request)
            
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Operación Curso *****
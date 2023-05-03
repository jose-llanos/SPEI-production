# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de fecha
from datetime import date, datetime
# Se importa la librería para envío de correos
from django.core.mail import EmailMessage

# Libreria para extraer el nombre de archivos en un directorio
import os

# Se importan las librerias para subir archivos .csv
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql


# ***** Seguimiento *****
def suggestion(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT course_name 
                           FROM early_intervention.courses
                           WHERE state = 'A' """)
        course = cursor.fetchall()

        # Se consultan los semestres
        cursor.execute(""" SELECT semester 
                           FROM early_intervention.semesters 
                           WHERE state = 'A' """)
        semester = cursor.fetchall()

        # Se consultan los estudiantes a intervenir
        cursor.execute(""" SELECT student 
                           FROM early_intervention.regression_data
                           WHERE id_semesters = 2
                           AND final_prediction < 4.1 """)
        student = cursor.fetchall()

        context = {"course":   course,
                   "semester": semester, 
                   "student":  student,
                   "user":     request.session['user'], 
                   "role":     request.session['role']}
        
        # *** Plantilla ***
        return render(request, 'proactive_intervention/suggestion.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Seguimiento *****



# ***** Seguimiento Estudiante *****
def student_suggestion(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        cmb_student = request.POST['cmbStudent']

        # Se consulta el id del semestre
        select = (""" SELECT id 
                      FROM early_intervention.semesters 
                      WHERE semester = %(semester)s 
                      AND state = 'A' """)
        cursor.execute(select, {'semester': cmb_semester})
        id_semester = cursor.fetchone()

        # Se ejecuta el query de la cabecera
        select = (""" SELECT T.id, T.id_semesters, T.student, 
                      T.id_reinforcement_workshop, RD.average, RD.final_prediction,
                      T.average_reinforcement
                      FROM early_intervention.tracking AS T, early_intervention.regression_data AS RD
                      WHERE T.student = RD.student
                      AND T.id_semesters = %s
                      AND T.student = %s """)
        parameter = (id_semester[0], cmb_student)
        cursor.execute(select, parameter)

        # Se cargan los registros del cursos
        head = cursor.fetchall()

        # Se ejecuta el query del cuerpo
        select = (""" SELECT TD.id_exercise, TD.id_state, TD.number_tried, 
                      TD.creation_date, TD.delivery_date, TD.court_date
                      FROM early_intervention.tracking_detail AS TD
                      INNER JOIN early_intervention.tracking AS T ON TD.id_tracking = T.id
                      WHERE T.id_semesters = %s
                      AND T.student = %s """)
        parameter = (id_semester[0], cmb_student)
        cursor.execute(select, parameter)

        # Se cargan los registros del cursos
        body = cursor.fetchall()

        # Defino los vectores para los elementos del reporte
        exercise = []
        state = []
        number_attemps = []

        for row in body:
            exercise.append(int(row[0]))
            if row[1] == 3:
                state.append(100)
            if row[1] == 2:
                state.append(50)
            if row[1] == 1:
                state.append(0)
            
            number_attemps.append(int(row[2]))

        context = {"head":           head, 
                   "body":           body, 
                   "exercise":       exercise, 
                   "state":          state, 
                   "number_attemps": number_attemps,
                   "user":           request.session['user'], 
                   "role":           request.session['role']}

        # *** Plantilla ***
        return render(request, 'proactive_intervention/suggestion.html', context=context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Seguimiento Estudiante *****
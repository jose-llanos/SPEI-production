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


# ***** Refuerzo *****
def reinforcement(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT id, course_name 
                           FROM early_intervention.courses
                           WHERE state = 'A' """)
        course = cursor.fetchall()

        # Se consultan los semestres
        cursor.execute(""" SELECT id, semester 
                           FROM early_intervention.semesters 
                           WHERE state = 'A' """)
        semester = cursor.fetchall()

        context = {"course":   course,
                   "semester": semester, 
                   "user":     request.session['user'], 
                   "role":     request.session['role']}
        
        # *** Plantilla ***
        return render(request, 'proactive_intervention/reinforcement.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Refuerzo *****



# ***** Refuerzo Estudiante *****
def student_reinforcement(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']

         # Se consulta el nombre del curso
        cursor.execute(""" SELECT id, course_name 
                           FROM early_intervention.courses
                           WHERE state = 'A' """)
        course = cursor.fetchall()

        # Se consultan los semestres
        cursor.execute(""" SELECT id, semester 
                           FROM early_intervention.semesters 
                           WHERE state = 'A' """)
        semester = cursor.fetchall()

        # Se consulta el id de courses_semesters
        select = (""" SELECT id 
                      FROM early_intervention.courses_semesters 
                      WHERE id_course = %s
                      AND id_semester = %s
                      AND state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Se consultan los registros para el refuerzo 
        select = (""" SELECT student, lab1, lab2, lab3, final_prediction 
                      FROM early_intervention.regression_data 
                      WHERE id_courses_semesters = %(id_courses_semesters)s
                      AND final_prediction < 4.1
                      ORDER BY final_prediction ASC """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
        record = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros
        context = {"course":   course,
                   "semester": semester,
                   "record":   record, 
                   "user":     request.session['user'], 
                   "role":     request.session['role']}

        # *** Plantilla ***
        return render(request, 'proactive_intervention/reinforcement.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Refuerzo Estudiante *****



# ***** Enviar Refuerzo Estudiante *****
def send_student_reinforcement(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']

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

        # Se consulta el id del semestre
        select = (""" SELECT id 
                      FROM early_intervention.semesters 
                      WHERE semester = %(semester)s 
                      AND state = 'A' """)
        cursor.execute(select, {'semester': cmb_semester})
        id_semester = cursor.fetchone()


        # Consulto los estudiantes con bajo desempeño para enviar el refuerzo
        cursor.execute(""" SELECT RD.student, u.email 
                           FROM early_intervention.regression_data AS RD, inginious.users AS U
                           WHERE RD.student = U.realname
                           AND RD.final_prediction < 3.0
                           ORDER BY RD.final_prediction ASC """)
        record = cursor.fetchall()

        low_performing_student = []
        student_email = []
        test_student_email = []

        for row in record:
            # Se concatena el nombre y correo del estudiante para el contexto
            student = row[0] +" - "+ row[1]
            low_performing_student.append(student)
            # Se carga en el vector el correo del estudiante para enviar el mensaje
            student_email.append(row[1])

        test_student_email.append('chepe159@gmail.com')

        # Enviar: Taller de Refuerzo 1 - Guía Asistida
        affair =     'FDP - Taller de Refuerzo 1 - Guía Asistida'
        message =    'Hola, lo invito a desarrollar el taller de refuerzo adjunto para el curso de FDP. El objetivo es mejorar el desempeño académico. El desarrollo de este taller tiene una nota apreciativa en el proyecto final. El plazo máximo de entrega es el 22 de diciembre de 2022.'
        email_from = 'ing.jose.llanos@gmail.com'
        email_to =   test_student_email
        reply_to =   'ing.jose.llanos@gmail.com'
        
        mail = EmailMessage(
            affair,
            message,
            email_from,
            email_to, 
        )
        mail.attach_file('SPEI/data/TallerRefuerzo1.pdf')
        mail.send()

        # Consulto los estudiantes con medio desempeño para enviar el refuerzo
        cursor.execute(""" SELECT RD.student, u.email 
                           FROM early_intervention.regression_data AS RD, inginious.users AS U
                           WHERE RD.student = U.realname
                           AND RD.final_prediction BETWEEN 3.0 AND 4.0
                           ORDER BY RD.final_prediction ASC """)
        record= cursor.fetchall()

        average_performing_student = []
        student_email = []

        for row in record:
            # Se concatena el nombre y correo del estudiante para el contexto
            student = row[0] +" - "+ row[1]
            average_performing_student.append(student)
            # Se carga en el vector el correo del estudiante para enviar el mensaje
            student_email.append(row[1])

        # Enviar: Taller de Refuerzo 2 - Pseudocodigo
        affair =     'FDP - Taller de Refuerzo 2 - Pseudocódigo'
        message =    'Hola, lo invito a desarrollar el taller de refuerzo adjunto para el curso de FDP. El objetivo es mejorar el desempeño académico. El desarrollo de este taller tiene una nota apreciativa en el proyecto final. El plazo máximo de entrega es el 22 de diciembre de 2022.'
        email_from = 'ing.jose.llanos@gmail.com'
        email_to =   test_student_email
        reply_to =   'ing.jose.llanos@gmail.com'
        
        mail = EmailMessage(
            affair,
            message,
            email_from,
            email_to, 
        )
        mail.attach_file('SPEI/data/TallerRefuerzo2.pdf')
        mail.send()

        # Se renderiza con el Contexto con los parámetros
        context = {"course":             course,
                   "semester":           semester, 
                   "low_performing":     low_performing_student, 
                   "average_performing": average_performing_student, 
                   "user":               request.session['user'], 
                   "role":               request.session['role']}
        
        # *** Plantilla ***
        return render(request, 'proactive_intervention/reinforcement.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Enviar Refuerzo Estudiante *****

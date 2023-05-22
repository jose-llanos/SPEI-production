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
        # FDP id_courses_semesters = 3
        if id_courses_semesters[0] == 3:
            student_in = ('JOSE RUBEN ORTIZ MARIN', 'HANNER YEFREY CHIRAN TAIMAL', 'JUAN ESTEBAN ARCE TOVAR',
                          'EDISON SNEYDER MOMPOTES TENORIO', 'CRISTIAN FERNEY JUASPUEZAN PUENAYAN', 'DANIEL ARTURO QUINTERO DIAZ',
                          'MIGUEL ANGEL PECHENE TOLEDO', 'JUAN JOSE BENAVIDES DIAZ', 'GILVER YESID ESCOBAR RODRIGUEZ',
                          'ROBERT SANTIAGO BANGUERO CANDELO', 'SANTIAGO GONGORA CUERO', 'JOSUE DUARTE HORMIGA',
                          'JHORDY ACEVEDO CABEZAS', 'BRAYAN STEBAN CUERO AGUDELO','JUAN DAVID JARAMILLO MOSQUERA','MARIA JULIANA MARIN SHEK')
            
        # FPOO id_courses_semesters = 5
        else:
            student_in = ('JUAN FELIPE FIGUEROA SERNA','SEBASTIAN ASAF TRUJILLO VILLAFANE','HELKIN GABRIEL JIMENEZ MEDINA',
                        'HAYDHEN ALBERTO CAMARGO ARIAS','ANDERSON FELIPE PANTOJA CADENA','JUAN SEBASTIAN TOBAR MORIONES',
                        'NESTOR DAVID BEDOYA HERMAN','MIGUEL ANGEL SALCEDO URIAN','ANDRES DAVID ORTEGA ARTEAGA',
                        'ALEJANDRO GARCIA GALLEGO','BAYRON RAFAEL RADA CABEZAS','ANDRES FELIPE ALCANTARA MUNOZ',
                        'LEONARDO CUADRO LOPEZ','JOSE DANIEL TRUJILLO SUAREZ','JOSE ADRIAN MARIN ORDONEZ',
                        'JAMES CALERO HURTADO','ELKIN SAMIR ANGULO PANAMENO','CESAR ALEJANDRO MUNOZ GUERRERO',
                        'BAYRON SEBASTIAN JOJOA ROSERO','WILLIAM DAVID HERNANDEZ SOLARTE','SANTIAGO RUIZ CORTES',
                        'RICARDO ERAZO MUNOZ','ALEXANDRA MARMOLEJO GOMEZ','SALOME ACOSTA MONTANO')

        select = (""" SELECT student, lab1, lab2, lab3, final_prediction 
                        FROM early_intervention.regression_data 
                        WHERE id_courses_semesters = %s
                        AND student IN %s
                        ORDER BY final_prediction ASC  """)
        parameter = (id_courses_semesters[0], student_in)
        cursor.execute(select, parameter)
        record = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros
        context = {"course":   cmb_course,
                   "semester": cmb_semester,
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

        # Se consulta el id de courses_semesters
        select = (""" SELECT id 
                      FROM early_intervention.courses_semesters 
                      WHERE id_course = %s
                      AND id_semester = %s
                      AND state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()


        
        # Consulto los estudiantes con bajo y medio desempeño para enviar el refuerzo
        # FDP id_courses_semesters = 3
        if id_courses_semesters[0] == 3:
            student_in = ('JOSE RUBEN ORTIZ MARIN', 'HANNER YEFREY CHIRAN TAIMAL', 'JUAN ESTEBAN ARCE TOVAR',
                          'EDISON SNEYDER MOMPOTES TENORIO', 'CRISTIAN FERNEY JUASPUEZAN PUENAYAN', 'DANIEL ARTURO QUINTERO DIAZ',
                          'MIGUEL ANGEL PECHENE TOLEDO', 'JUAN JOSE BENAVIDES DIAZ', 'GILVER YESID ESCOBAR RODRIGUEZ',
                          'ROBERT SANTIAGO BANGUERO CANDELO', 'SANTIAGO GONGORA CUERO', 'JOSUE DUARTE HORMIGA',
                          'JHORDY ACEVEDO CABEZAS', 'BRAYAN STEBAN CUERO AGUDELO','JUAN DAVID JARAMILLO MOSQUERA','MARIA JULIANA MARIN SHEK')
            indicator_achievement_in = (10, 11, 2, 4, 6)
        # FPOO id_courses_semesters = 5
        else:
            student_in = ('JUAN FELIPE FIGUEROA SERNA','SEBASTIAN ASAF TRUJILLO VILLAFANE','HELKIN GABRIEL JIMENEZ MEDINA',
                        'HAYDHEN ALBERTO CAMARGO ARIAS','ANDERSON FELIPE PANTOJA CADENA','JUAN SEBASTIAN TOBAR MORIONES',
                        'NESTOR DAVID BEDOYA HERMAN','MIGUEL ANGEL SALCEDO URIAN','ANDRES DAVID ORTEGA ARTEAGA',
                        'ALEJANDRO GARCIA GALLEGO','BAYRON RAFAEL RADA CABEZAS','ANDRES FELIPE ALCANTARA MUNOZ',
                        'LEONARDO CUADRO LOPEZ','JOSE DANIEL TRUJILLO SUAREZ','JOSE ADRIAN MARIN ORDONEZ',
                        'JAMES CALERO HURTADO','ELKIN SAMIR ANGULO PANAMENO','CESAR ALEJANDRO MUNOZ GUERRERO',
                        'BAYRON SEBASTIAN JOJOA ROSERO','WILLIAM DAVID HERNANDEZ SOLARTE','SANTIAGO RUIZ CORTES',
                        'RICARDO ERAZO MUNOZ','ALEXANDRA MARMOLEJO GOMEZ','SALOME ACOSTA MONTANO')
            indicator_achievement_in = (16, 17, 18, 23, 24)


        select = (""" SELECT RD.student, u.email 
                           FROM early_intervention.regression_data AS RD, inginious.users AS U
                           WHERE RD.student = U.realname
                           AND RD.student IN %(student_in)s
                           ORDER BY RD.final_prediction ASC """)
        cursor.execute(select, {'student_in': student_in})
        record = cursor.fetchall()

        student_performance  = []
        
        # Se envía el mensaje a cada estudiante
        for row in record:
            # Lista para el nombre de los ejercicios de refuerzo
            reinforcement_exercise = []
            student_email = []

            # Se concatena el nombre y correo del estudiante para el contexto
            student = row[0] +" - "+ row[1]
            student_performance.append(student)

            # Se extrae el nombre de los talleres de refuerzo
            select = ("""SELECT DISTINCT EA.reinforcement_exercise
                               FROM early_intervention.evaluation_activity AS EA
                               INNER JOIN early_intervention.student_assessments AS SA ON EA.id = SA.id_evaluation_activity
                               AND SA.grade_indicator <= (EA.points / 2)
                               WHERE EA.id_indicator_achievement IN %s
                               AND SA.student_name = %s """)
            parameter = (indicator_achievement_in, row[0])
            cursor.execute(select, parameter)
            record_exercise = cursor.fetchall()
            
            for exercise in record_exercise:
                # Se carga el nombre de los ejercicios de refuerzo
                reinforcement_exercise.append(exercise[0])

            # Se carga el correo del estudiante para enviar el mensaje
            student_email.append(row[1])
            student_email.append('ing.jose.llanos@gmail.com')

            # Enviar: Taller de Refuerzo 1 - Guía Asistida
            affair   =   'FDP - Talleres de Refuerzo'
            message  =   'Hola, l@ invito a desarrollar los ejercicios de refuerzo (INGInious):'+ str(reinforcement_exercise)
            message +=   '\n\nEl objetivo de estos talleres es mejorar el desempeño académico. ' 
            message +=   'El plazo máximo de entrega es el 17 de mayo de 2023 y tiene una calificación apreciativa en la calificación final del curso.'
            #message +=   '\n\nAdjunto las guías de refuerzo: entradas/salidas, condiciones y funciones.'
            message +=   '\n\nSaludos,'
            email_from = 'ing.jose.llanos@gmail.com'
            email_to =   student_email
            
            mail = EmailMessage(
                affair,
                message,
                email_from,
                email_to
            )
            #mail.attach_file('SPEI/data/GuiaRefuerzo1-entradas-salidas.pdf')
            #mail.attach_file('SPEI/data/GuiaRefuerzo2-condiciones.pdf')
            #mail.attach_file('SPEI/data/GuiaRefuerzo3-funciones.pdf')
            mail.send()

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

        # Se renderiza con el Contexto con los parámetros
        context = {"course":                  course,
                   "semester":                semester, 
                   "student_performance":     student_performance, 
                   "user":                    request.session['user'], 
                   "role":                    request.session['role']}
        
        # *** Plantilla ***
        return render(request, 'proactive_intervention/reinforcement.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Enviar Refuerzo Estudiante *****

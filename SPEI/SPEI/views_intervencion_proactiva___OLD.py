# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería para envío de correos
from django.core.mail import EmailMessage
# Se importa la librería de tiempo
import datetime

# Libreria para extraer el nombre de archivos en un directorio
import os

# Se importan las librerias para subir archivos .csv
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql

# Se importan las librerías 
import numpy as np 
import pandas as pd


# ***** Subir Calificaciones Intervención Proactiva *****
def upload_grades_proactive_intervention(request):
    # Validación de variables de sesión
    try:
        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'subir_calificaciones.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Subir Calificaciones Intervención Proactiva *****


# ***** Subir Plano Intervención Proactiva *****
def upload_plane_proactive_intervention(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        curso = request.POST['cmbCurso']
        semestre = request.POST['cmbSemestre']

        # Se valida si existe el archivo en el directorio /media
        archivos = os.listdir('/Users/josellanos/Documents/GitHub/JMLM/Django/SPEI/media')

        # Contador para validar los archivos dentro del directorio
        contador_archivo = 0
        nombre_archivo = str(request.FILES['myfile'])

        for i in archivos:
            # Si en el directorio existe un archivo con el mismo nombre del .csv
            if i == nombre_archivo:
                # El contador se incrementa
                contador_archivo = contador_archivo + 1

        # Si contador es igual a 0, se carga el archivo .csv en el directorio, porque no existe
        uploaded_file_url = ""
        
        if contador_archivo == 0:
            # *** Se sube el archivo .csv a la carpeta /media ***
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
            # *** Fin insertar archivo .csv ***

        # url del archivo
        url_archivo = "/Users/josellanos/Documents/GitHub/JMLM/Django/SPEI/media/" + nombre_archivo

        # Se lee el archivo plano
        data = pd.read_csv(url_archivo , sep=';')

        # Se convierte el DataFrame a una lista
        result = data.to_numpy().tolist()

        # Se valida si existen registros para ese curso y semestre
        select = (""" SELECT count(*) AS contador 
                    FROM early_intervention.grades 
                    WHERE course_id = %s AND semester = %s """)
        parametros = (curso, semestre)
        cursor.execute(select, parametros)

        registros = cursor.fetchall()

        # Se carga la variable contador para realizar la validación
        for row in registros:
            contador = row[0]

        # Si contador es igual a 0, entonces no existen registros en la tabla y se realiza el insert
        if contador == 0 :
            # Se inserta los registros del DataFrame a la tabla calificaciones
            for i in data.index:
                # Se calcula el promedio de las calificaciones para cada estudiante
                promedio = round((data['lab1'][i] + data['lab2'][i] + data['lab3'][i]) / 3, 1)
                
                # Se ejecuta el query 
                insert = (""" INSERT INTO early_intervention.grades (course_id, semester, student, lab1, 
                                                        delivery_time_lab1, number_tried_lab1,
                                                        lab2, lab3, average, final_prediction) 
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) """)
                parametros = (curso, semestre, data['student'][i], data['lab1'][i], data['delivery_time_lab1'][i], 
                            data['number_tried_lab1'][i], data['lab2'][i], data['lab3'][i], promedio,'0.0')

                cursor.execute(insert, parametros)

                

        # Se consultan los registros de la tabla para mostrarlos en el html
        select = (""" SELECT course_id, semester, student, lab1, 
                      delivery_time_lab1, number_tried_lab1, lab2, lab3
                      FROM early_intervention.grades 
                      WHERE course_id = %s AND semester = %s """)
        parametros = (curso, semestre)
        cursor.execute(select, parametros)

        registros = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros
        context = {"uploaded_file_url": uploaded_file_url, "datos": registros, "usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'subir_calificaciones.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Subir Plano Intervención Proactiva ***** 

# ***** Refuerzo *****
def refuerzo(request):
    # Validación de variables de sesión
    try:
        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'refuerzos.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Refuerzo *****

# ***** Refuerzo Estudiante *****
def refuerzo_estudiante(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cursos = request.POST['cmbCurso']
        semestres = request.POST['cmbSemestre']

        # Se ejecuta el query 
        select = (""" SELECT * 
                      FROM early_intervention.grades 
                      WHERE course_id = %s AND semester = %s
                      AND final_prediction < 4.1
                      ORDER BY final_prediction ASC """)
        parametros = (cursos,semestres)
        cursor.execute(select, parametros)

        # Se cargan los registros del cursos
        registros = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros
        context = {"datos": registros, "usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'refuerzos.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Refuerzo Estudiante *****

# ***** Enviar Refuerzo Estudiante *****
def enviar_refuerzo_estudiante(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cursos = 'FDP'
        semestres = '2022-2'

        # Consulto los estudiantes con bajo desempeño para enviar el refuerzo
        cursor.execute(""" SELECT c.student, u.email 
                           FROM early_intervention.grades AS c, inginious.users AS u
                           WHERE c.student = u.realname
                           AND final_prediction < 3.0
                           ORDER BY final_prediction ASC """)

        # Se cargan los registros
        registro = cursor.fetchall()

        estudiante_bajo_desempeno = []
        email_estudiante = []

        for row in registro:
            # Se concatena el nombre y correo del estudiante para el contexto
            estudiante = row[0] +" - "+ row[1]
            estudiante_bajo_desempeno.append(estudiante)
            # Se carga en el vector el correo del estudiante para enviar el mensaje
            email_estudiante.append(row[1])

        email_estudiante.append('chepe159@gmail.com')

        # Enviar: Taller de Refuerzo 1 - Guía Asistida
        asunto = 'FDP - Taller de Refuerzo 1 - Guía Asistida'
        mensaje = 'Hola, lo invito a desarrollar el taller de refuerzo adjunto para el curso de FDP. El objetivo es mejorar el desempeño académico. El desarrollo de este taller tiene una nota apreciativa en el proyecto final. El plazo máximo de entrega es el 22 de diciembre de 2022.'
        email_from = 'ing.jose.llanos@gmail.com'
        email_to = email_estudiante #['chepe159@gmail.com']
        reply_to = 'ing.jose.llanos@gmail.com'
        
        mail = EmailMessage(
            asunto,
            mensaje,
            email_from,
            email_to, 
        )
        mail.attach_file('SPEI/data/TallerRefuerzo1.pdf')
        mail.send()


        # Consulto los estudiantes con medio desempeño para enviar el refuerzo
        cursor.execute(""" SELECT c.student, u.email 
                           FROM early_intervention.grades AS c, inginious.users AS u
                           WHERE c.student = u.realname
                           AND final_prediction BETWEEN 3.0 AND 4.0
                           ORDER BY final_prediction ASC """)

        # Se cargan los registros
        registro = cursor.fetchall()

        estudiante_medio_desempeno = []
        email_estudiante = []

        for row in registro:
            # Se concatena el nombre y correo del estudiante para el contexto
            estudiante = row[0] +" - "+ row[1]
            estudiante_medio_desempeno.append(estudiante)
            # Se carga en el vector el correo del estudiante para enviar el mensaje
            email_estudiante.append(row[1])

        email_estudiante.append('chepe159@gmail.com')

        # Enviar: Taller de Refuerzo 2 - Pseudocodigo
        asunto = 'FDP - Taller de Refuerzo 2 - Pseudocódigo'
        mensaje = 'Hola, lo invito a desarrollar el taller de refuerzo adjunto para el curso de FDP. El objetivo es mejorar el desempeño académico. El desarrollo de este taller tiene una nota apreciativa en el proyecto final. El plazo máximo de entrega es el 22 de diciembre de 2022.'
        email_from = 'ing.jose.llanos@gmail.com'
        email_to = email_estudiante #['chepe159@gmail.com'] 
        reply_to = 'ing.jose.llanos@gmail.com'
        
        mail = EmailMessage(
            asunto,
            mensaje,
            email_from,
            email_to, 
        )
        mail.attach_file('SPEI/data/TallerRefuerzo2.pdf')
        mail.send()

        # Se renderiza con el Contexto con los parámetros
        context = {"bajo_desempeno": estudiante_bajo_desempeno, 
                   "medio_desempeno": estudiante_medio_desempeno, 
                   "usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'refuerzos.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Enviar Refuerzo Estudiante *****

# ***** Seguimiento *****
def seguimiento(request):
    # Validación de variables de sesión
    try:
        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'seguimientos.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Seguimiento *****

# ***** Seguimiento Estudiante *****
def seguimiento_estudiante(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cursos = request.POST['cmbCurso']
        semestres = request.POST['cmbSemestre']
        estudiante = request.POST['cmbEstudiante']

        # Se ejecuta el query de la cabecera
        select = (""" SELECT s.id, s.course_id, s.semester, s.student, 
                      s.id_reinforcement_workshop, c.average, c.final_prediction,
                      s.average_reinforcement
                      FROM early_intervention.tracking AS s, early_intervention.grades AS c
                      WHERE s.student = c.student
                      AND s.course_id = %s
                      AND s.semester = %s
                      AND s.student = %s """)
        parametros = (cursos,semestres, estudiante)
        cursor.execute(select, parametros)

        # Se cargan los registros del cursos
        registro_cabecera = cursor.fetchall()

        # Se ejecuta el query del cuerpo
        select = (""" SELECT sd.id_exercise, sd.id_state, sd.number_tried, 
                      sd.creation_date, sd.delivery_date, sd.court_date
                      FROM early_intervention.tracking AS s, early_intervention.tracking_detail AS sd
                      WHERE s.id = sd.id_tracking
                      AND s.course_id = %s
                      AND s.semester = %s
                      AND s.student = %s """)
        parametros = (cursos,semestres, estudiante)
        cursor.execute(select, parametros)

        # Se cargan los registros del cursos
        registro_cuerpo = cursor.fetchall()

        # Defino los vectores para los elementos del reporte
        ejercicio = []
        estado = []
        numero_intentos = []

        for row in registro_cuerpo:
            ejercicio.append(int(row[0]))
            if row[1] == 3:
                estado.append(100)
            if row[1] == 2:
                estado.append(50)
            if row[1] == 1:
                estado.append(0)
            
            numero_intentos.append(int(row[2]))

        context = {"cabecera": registro_cabecera, "cuerpo": registro_cuerpo, 
                "ejercicios": ejercicio, "estados": estado, "intentos": numero_intentos,
                "usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'seguimientos.html', context=context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Seguimiento Estudiante *****
# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de fecha
from datetime import date, datetime

# Libreria para extraer el nombre de archivos en un directorio
import os

# Se importan las librerias para subir archivos .csv
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Se importan las librerías 
import pandas as pd 

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql


# ***** Subir Calificaciones Intervención Proactiva *****
def record_proactive_intervention(request):
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
        return render(request, 'proactive_intervention/record_proactive_intervention.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Subir Calificaciones Intervención Proactiva *****


# ***** Subir Plano Intervención Proactiva *****
def upload_record_proactive_intervention(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']

        # Se valida si existe el archivo en el directorio /media
        file = os.listdir('/Users/josellanos/Documents/GitHub/JMLM/Django/SPEI/media')

        # Contador para validar los archivos dentro del directorio
        file_counter = 0
        file_name = str(request.FILES['myfile'])

        for i in file:
            # Si en el directorio existe un archivo con el mismo nombre del .csv
            if i == file_name:
                # El contador se incrementa
                file_counter = file_counter + 1

        # Si contador es igual a 0, se carga el archivo .csv en el directorio, porque no existe
        uploaded_file_url = ""
        
        if file_counter == 0:
            # *** Se sube el archivo .csv a la carpeta /media ***
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
            # *** Fin insertar archivo .csv ***

        # url del archivo
        url_archivo = "/Users/josellanos/Documents/GitHub/JMLM/Django/SPEI/media/" + file_name

        # Se lee el archivo plano
        data = pd.read_csv(url_archivo , sep=';')

        # Se convierte el DataFrame a una lista
        result = data.to_numpy().tolist()

        # Se consulta el id de courses_semesters
        select = (""" SELECT id 
                      FROM early_intervention.courses_semesters 
                      WHERE id_course = %s
                      AND id_semester = %s
                      AND state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Se valida si existen registros para ese semestre
        select = (""" SELECT count(*) AS contador 
                      FROM early_intervention.regression_data
                      WHERE id_courses_semesters = %(id_courses_semester)s """)
        cursor.execute(select, {'id_courses_semester': id_courses_semesters[0]})
        counter = cursor.fetchone()

        # Si contador es igual a 0, entonces no existen registros en la tabla y se realiza el insert
        if counter[0] == 0 :
            # Se inserta los registros del DataFrame a la tabla calificaciones
            for i in data.index:
                # Se calcula el promedio de las calificaciones para cada estudiante
                average = round((data['lab1'][i] + data['lab2'][i] + data['lab3'][i]) / 3, 1)
                
                # Se ejecuta el query 
                insert = (""" INSERT INTO early_intervention.regression_data 
                              (id_courses_semesters, student, lab1, 
                              delivery_time_lab1, number_tried_lab1,
                              lab2, lab3, average, final_prediction) 
                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) """)
                parameter = (str(id_courses_semesters[0]), 
                             str(data['student'][i]), 
                             str(data['lab1'][i]), 
                             str(data['delivery_time_lab1'][i]), 
                             str(data['number_tried_lab1'][i]), 
                             str(data['lab2'][i]), 
                             str(data['lab3'][i]), 
                             str(average),
                             '0.0')
                cursor.execute(insert, parameter)   

        # Se consultan los registros de la tabla para mostrarlos en el html
        select = (""" SELECT CS.id, RD.student, RD.lab1, 
                        RD.delivery_time_lab1, RD.number_tried_lab1, RD.lab2, RD.lab3
                        FROM early_intervention.regression_data AS RD
                        INNER JOIN early_intervention.courses_semesters AS CS ON RD.id_courses_semesters = CS.id
                        WHERE RD.id_courses_semesters = %(id_courses_semesters)s """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
        record = cursor.fetchall()

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
        context = {"course":            course,
                   "semester":          semester,
                   "uploaded_file_url": uploaded_file_url, 
                   "record":            record, 
                   "user":              request.session['user'], 
                   "role":              request.session['role']}
        
        # *** Plantilla ***
        return render(request, 'proactive_intervention/record_proactive_intervention.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Subir Plano Intervención Proactiva ***** 
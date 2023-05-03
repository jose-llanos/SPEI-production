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



# ***** Plano Intervención Preventiva *****
def record_preventive_intervention(request):
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
        return render(request, 'preventive_intervention/record_preventive_intervention.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Plano Intervención Preventiva *****


# ***** Subir Registros Intervención Preventiva *****
def upload_record_preventive_intervention(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']

        # Se genera la homologación del curso y las tareas con INGInious
        taskid = []
        if cmb_course == '1':
            courseid = 'FDP-01-2023-1'
            taskid = 'Lab1-Problema1'
            taskid += 'Lab1-Problema2'
        elif cmb_course == '2':
            courseid = 'FPOO-Victor-2023-1'
            taskid = 'Laboratorio1'
        else:
            print("El CURSO o el SEMESTRE no existen en la BD SPEI")

        print("taskid:::", taskid)

        ##### Validación y cargue del archivo plano ##### 

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


        ##### Validación y cargue de los registros ##### 

        # Se consulta el id de courses_semesters
        select = (""" SELECT id 
                      FROM early_intervention.courses_semesters 
                      WHERE id_course = %s
                      AND id_semester = %s
                      AND state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Se valida si existen registros para courses_semesters
        select = (""" SELECT count(*) AS counter
                      FROM early_intervention.classification_data 
                      WHERE id_courses_semesters = %(id_courses_semesters)s """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
        counter = cursor.fetchone()
        
        # Si contador es igual a 0, entonces no existen registros en la tabla y se realiza el insert
        if counter[0] == 0 :
            # Se consulta la fecha de presentación de la actividad
            select = (""" SELECT date_presentation
                          FROM early_intervention.tasks_log
                          WHERE id_courses_semesters =  %(id_courses_semesters)s """)
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            date_presentation = cursor.fetchone()

            date_presentation = str(date_presentation[0])
            date_presentation = date_presentation[0:19]

            # Se recorren los elementos del archivo plano
            for i in data.index:
                # Se busca el nombre de usuario del estudiante en INGInious
                select = (""" SELECT username
                              FROM inginious.users
                              WHERE realname like %(student)s """)
                cursor.execute(select, {'student': data['student'][i]})
                username = cursor.fetchone()

                ##### Se calcula el tiempo utilizado en las actividades (por día) #####

                # Se consulta el tiempo utilizado por el estudiante en el Laboratorio 1
                select = (""" SELECT submitted_on
                              FROM inginious.submissions
                              WHERE courseid = %s
                              AND taskid IN (%s)
                              AND username = %s
                              ORDER BY submitted_on DESC 
                              LIMIT 1 """)
                parameter = (courseid,
                             taskid,
                             username[0])
                cursor.execute(select, parameter)
                submitted_on = cursor.fetchone()

                
                # Si el estudiante no presentó la actividad, activity_completion_date es igual date_presentation[0]
                if submitted_on == None:
                    activity_completion_date = date_presentation
                # Sino activity_completion_date es igual a la última fecha de la presentación
                else:
                    activity_completion_date = submitted_on[0]
                
                # Se define el formato para la fecha
                date_format_str = "%Y-%m-%d %H:%M:%S"

                activity_completion_date = str(activity_completion_date)
                activity_completion_date = activity_completion_date[0:19]

                # Se define la fecha de inicio y fin para restar
                start = datetime.strptime(date_presentation, date_format_str)
                end =   datetime.strptime(activity_completion_date, date_format_str)

                # Se restan las fechas para obtener el valor de días
                diff = end - start
                
                # Se calcula el tiempo en días
                diff_in_day = diff.total_seconds() / 86400

                ##### Se calcula el número de intentos por actividad (laboratorio 1) ##### 
                select = (""" SELECT avg(tried) AS tried
                              FROM inginious.user_tasks 
                              WHERE course_id = %s
                              AND taskid IN (%s)
                              AND username = %s
                              GROUP BY username """)
                parameter = (courseid,
                             taskid,
                             username[0])
                cursor.execute(select, parameter)
                number_tried = cursor.fetchone()

                # Si el estudiante no presentó la actividad, intentos es igual a cero
                if number_tried == None:
                    number_tried = 0
                # Sino es igual al valor de la consulta
                else:
                    number_tried = number_tried[0]

                ###### print("Student: ", data['student'][i] , " - Numero Intentos:::::", round(number_tried, 0))

                ##### Se obtiene el resultado para el laboratorio ####

                # Se consulta el grade y el tried para obtener el resultado del laboratorio
                select = (""" SELECT avg(grade) AS grade, sum(tried) AS tried
                              FROM inginious.user_tasks
                              WHERE course_id = %s
                              AND taskid IN (%s) 
                              AND username = %s """)
                parameter = (courseid,
                             taskid,
                             username[0])
                cursor.execute(select, parameter)
                result = cursor.fetchone()

                if result[0] == None:
                    grade = 0
                else:
                    grade = round(result[0], 0)

                if result[0] == None:
                    tried = 0
                else:
                    tried = round(result[1], 0)

                #print("UserName:::", username)
                #print("......................")
                #print("Grade:::", grade)
                #print("Tried:::", tried)

                # Si grade = 100 y tried >= 1  --> presentó y paso (3)
                if grade == 100 and tried >= 1:
                    result_lab = 3
                # Sino grade >= 0 y tried > 0 --> Presentó y fallo (1)
                elif grade >= 0 and tried > 0:
                    result_lab = 1
                # Sino grade = 0 y tried = 0 --> No presentó (0)
                else:
                    result_lab = 0

                # Se inserta el registro para la predicción de la semana 3 
                insert_week3 = (""" INSERT INTO early_intervention.classification_data 
                                    (id_courses_semesters, week_prediction, student, lab1, 
                                    delivery_time_lab1, number_tried_lab1, result_lab1, 
                                    lab2, prediction)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) """)
                parameter = (id_courses_semesters[0], 
                             '3', 
                             str(data['student'][i]), 
                             str(data['lab1'][i]),
                             round(diff_in_day,2), 
                             round(number_tried, 0), 
                             result_lab, 
                             str(data['lab2'][i]),
                             '-1')
                cursor.execute(insert_week3, parameter)
                 
                # Se inserta el registro para la predicción de la semana 5 
                insert_week5 = (""" INSERT INTO early_intervention.classification_data 
                                    (id_courses_semesters, week_prediction, student, lab1, 
                                    delivery_time_lab1, number_tried_lab1, result_lab1, 
                                    lab2, prediction)
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) """)
                parameter = (id_courses_semesters[0], 
                             '5', 
                             str(data['student'][i]), 
                             str(data['lab1'][i]),
                             round(diff_in_day,2), 
                             round(number_tried, 0), 
                             result_lab, 
                             str(data['lab2'][i]), 
                             '-1')
                cursor.execute(insert_week5, parameter)     

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
   
        # Se consultan los registros de la tabla para mostrarlos en el html
        select = (""" SELECT DISTINCT C.course_acronym, S.semester, CD.student, CD.lab1, CD.delivery_time_lab1, 
                      CD.number_tried_lab1, CD.result_lab1, CD.lab2 
                      FROM early_intervention.classification_data AS CD
                      INNER JOIN early_intervention.courses_semesters AS CS ON CD.id_courses_semesters = CS.id
                      INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id
                      INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                      WHERE CD.id_courses_semesters =  %(id_courses_semesters)s 
                      ORDER BY CD.student ASC """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})

        record = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros 
        context = {"course":            course,
                   "semester":          semester,
                   "uploaded_file_url": uploaded_file_url, 
                   "record":            record,
                   "user":              request.session['user'], 
                   "role":              request.session['role']}

        # *** Plantilla ***
        return render(request, 'preventive_intervention/record_preventive_intervention.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Subir Registros Intervención Preventiva *****
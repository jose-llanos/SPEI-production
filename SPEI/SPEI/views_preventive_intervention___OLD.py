# Se importan las libreria de template
#from re import I
from django.shortcuts import render
# Se importa la librería para envío de correos
from django.core.mail import EmailMessage
# Se importa la librería de fecha
from datetime import date, datetime

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

# libreria para Bosque Aleatorio
from sklearn.ensemble import RandomForestClassifier

# Se importa la libreria para dividir los datos de entrenamiento y de pruebas
from sklearn.model_selection import train_test_split
# Genera la matriz de confusión
from sklearn.metrics import confusion_matrix
# Gerera el reporte de la clasificación
from sklearn.metrics import classification_report




# ***** Plano Intervención Preventiva *****
def plane_preventive_intervention(request):
    # Validación de variables de sesión
    try:
        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'plane_preventive_intervention.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Plano Intervención Preventiva *****





# ***** Subir Registros Intervención Preventiva *****
def upload_records_preventive_intervention(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cursos = request.POST['cmbCurso']
        semestres = request.POST['cmbSemestre']
        curso_id = cursos+ "-" +semestres

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
                      FROM early_intervention.classification_data 
                      WHERE course_id = %(cursoid)s """)
        cursor.execute(select, {'cursoid': curso_id})

        # Se carga la variable contador para realizar la validación
        for row in cursor.fetchall():
            contador = row[0]

        # Si contador es igual a 0, entonces no existen registros en la tabla y se realiza el insert
        if contador == 0 :
            # Se inserta los registros del DataFrame a la tabla calificaciones
            for i in data.index:
                # Se inserta el registro para la predicción de la semana 3 
                insert_semana3 = (""" INSERT INTO early_intervention.classification_data (course_id, week_prediction, 
                              student, lab1, delivery_time_lab1, number_tried_lab1, result_lab1, lab2, prediction)
                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) """)
                parametros = (curso_id, '3', data['student'][i], data['lab1'][i], 
                              data['delivery_time_lab1'][i], str(data['number_tried_lab1'][i]), 
                              str(data['result_lab1'][i]), str(data['lab2'][i]), '-1')
                cursor.execute(insert_semana3, parametros)

                # Se inserta el registro para la predicción de la semana 5 
                insert_semana5 = (""" INSERT INTO early_intervention.classification_data (course_id, week_prediction, 
                              student, lab1, delivery_time_lab1, number_tried_lab1, result_lab1, lab2, prediction)
                              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) """)
                parametros = (curso_id, '5', data['student'][i], data['lab1'][i], 
                              data['delivery_time_lab1'][i], str(data['number_tried_lab1'][i]), 
                              str(data['result_lab1'][i]), str(data['lab2'][i]), '-1')
                cursor.execute(insert_semana5, parametros)
            
        
        # Se consultan los registros de la tabla para mostrarlos en el html
        select = (""" SELECT DISTINCT course_id, student, lab1, delivery_time_lab1, number_tried_lab1, result_lab1, lab2 
                      FROM early_intervention.classification_data 
                      WHERE course_id = %(cursoid)s """)
        cursor.execute(select, {'cursoid': curso_id})

        registros = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros 
        context = {"uploaded_file_url": uploaded_file_url, "datos": registros, "usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'plane_preventive_intervention.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Subir Registros Intervención Preventiva *****





# ***** Clasificación Desempeño Estudiante *****
def performance_classification(request):
    # Validación de variables de sesión
    try:
        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'performance_classification.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Clasificación Desempeño Estudiante *****





# ***** Predición Clasificacion Desempeño *****
def performance_classification_prediction(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        curso = request.POST['cmbCurso']
        semestre = request.POST['cmbSemestre']
        curso_id = curso + "-" + semestre
        semana = request.POST['cmbSemana']

        # Se cargan los datos
        data = pd.read_csv("SPEI/data/entrenamiento_clasificacion_468.csv", sep=';')

        # Se limpian los datos
        data = data.dropna()

        # Se realiza el resample de los datos
        from sklearn.utils import resample

        # 189
        '''
        df_bajo = data[data['Grade2'] == 0]
        df_medio = data[data['Grade2'] == 1]
        df_alto = data[data['Grade2'] == 2]

        data_resample_medio = resample(df_medio,
                        replace = True,
                        n_samples = 101,
                        random_state = 1)

        data_resample_alto = resample(df_alto,
                        replace = True,
                        n_samples = 101,
                        random_state = 1)

        data2 = pd.concat([df_bajo, data_resample_medio, data_resample_alto])
        '''

        # 468
        df_bajo = data[data['grade'] == 0]
        df_medio = data[data['grade'] == 1]
        df_alto = data[data['grade'] == 2]

        df_bajo = data[data['grade'] == 0]
        df_medio = data[data['grade'] == 1]
        df_alto = data[data['grade'] == 2]

        data_resample_bajo = resample(df_bajo,
                        replace = True,
                        n_samples = 200,
                        random_state = 1)

        data_resample_alto = resample(df_alto,
                        replace = True,
                        n_samples = 200,
                        random_state = 1)

        data2 = pd.concat([data_resample_bajo, df_medio, data_resample_alto])

        # Se seleccionan las características según la semana
        if semana == '3':
            # Selección de características y clase para la semana 3
            features = ['lab_1','tiempo_entrega_lab_1','intentos_lab_1']
            X = data2[features] 
            y = data2['grade'].values

            # Se dividen los datos para el entrenamiento (80% entrenamiento y 20% pruebas)
            X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        train_size = 0.8, 
                                                        random_state= 1)

            # Se crea el modelo 
            rf = RandomForestClassifier(bootstrap=False, max_depth=100, min_samples_split=10)
        else:
            # Selección de características y clase para la semana 5
            features = ['lab_1','tiempo_entrega_lab_1','intentos_lab_1','lab_2']
            X = data2[features] 
            y = data2['grade'].values

            # Se dividen los datos para el entrenamiento (80% entrenamiento y 20% pruebas)
            X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                        train_size = 0.8, 
                                                        random_state= 1)

            # Se crea el modelo 
            rf = RandomForestClassifier(max_depth=20, max_features='log2', n_estimators=20)

        # Se entrena el modelo
        rf.fit(X_train, y_train)

        pred = rf.predict(X_test)

        # Se imprime la matriz de confusión
        #print(confusion_matrix(y_test, pred))

        # Se imprime la precisión del modelo
        print(classification_report(y_test, pred))

        '''
        # Ejemplo Predicción
        #lab1 = [5.0, 5.0, 0.0, 5.0, 5.0, 0.0]
        #tiempo_entrega = [10.24, 20.18, 0.00, 12.96, 15.91, 9.11]
        #cantidad_intentos = [4, 4, 0, 4, 4, 4]
        #tipo_matricula = [1, 1, 0, 1, 1, 1]
        
        lab1 = [5.0, 5.0, 5.0, 5.0]
        tiempo_entrega = [0.5, 0.70, 1.45, 7.04]
        cantidad_intentos = [5, 5, 5, 5]
        tipo_matricula = [1, 1, 1, 1]


        y = pd.DataFrame({'Laboratorio-1': lab1, 'Tiempo-Entrega-Lab1': tiempo_entrega, 
                        'Cantidad-Intentos-Lab1': cantidad_intentos, 'Tipo-Matricula': tipo_matricula})

        x = rf.predict(y)

        print("Predicción: Desempeño Estudiante RFC = ", x)
        '''
        ### -----------------------------------------------

        # Se consulta el valor de la predicción
        select = (""" SELECT prediction 
                      FROM early_intervention.classification_data
                      WHERE course_id = %s 
                      AND week_prediction = %s """)
        parametros = (curso_id, semana)
        cursor.execute(select, parametros)

        # Se carga la variable predicción para realizar la validación
        for row in cursor.fetchall():
            prediccion = row[0]

        # Si predicción es igual a -1, entonces se realiza la predicción
        if prediccion == -1 :
            # se selecciona la semana a predecir
            # Si la semana es igual a 3
            if semana == '3':
                # Se cargan los registros 
                select = (""" SELECT student, lab1, delivery_time_lab1, number_tried_lab1
                            FROM early_intervention.classification_data
                            WHERE course_id = %s 
                            AND week_prediction = %s """)
                parametros = (curso_id, semana)
                cursor.execute(select, parametros)

                # Se cargan los registros del cursor
                registros = cursor.fetchall()
                
                # Se cargan los registros en un DataFrame
                data = pd.DataFrame(registros, 
                                    columns=['student','lab_1','tiempo_entrega_lab_1','intentos_lab_1'])
                                                    
                # Se seleccionan los datos para predecir
                test = data.drop(['student'], axis= 1)

                # Se genera la predicción para el curso
                prediccion = rf.predict(test)

                # Se adiciona la columna: Predicción al DataFrame
                prediccion = pd.DataFrame(prediccion,columns=['prediction'])
        
                # Se concatena en el DataFrame con el estudiante y la predicción
                result= pd.concat([data['student'], prediccion], axis=1)

                # Se ordenan los valores por la columna prediccion de menor a mayor
                result = result.sort_values('prediction')

                # Se actualiza final_prediccion en la tabla calificaciones de la BD
                for i in result.index:
                    update = """ UPDATE early_intervention.classification_data SET prediction = %s 
                                 WHERE course_id = %s
                                 AND week_prediction = %s
                                 AND student = %s """
                    parametros = (str(result['prediction'][i]),
                                  curso_id,
                                  semana,
                                  result['student'][i])
                    cursor.execute(update, parametros)

            # Sino la semana es igual a 5
            else:
                # Se cargan los registros 
                select = (""" SELECT student, lab1, delivery_time_lab1, number_tried_lab1, lab2
                              FROM early_intervention.classification_data
                              WHERE course_id = %s 
                              AND week_prediction = %s """)
                parametros = (curso_id, semana)
                cursor.execute(select, parametros)

                # Se cargan los registros del cursor
                registros = cursor.fetchall()
                
                # Se cargan los registros en un DataFrame
                data = pd.DataFrame(registros, 
                                    columns=['student','lab_1','tiempo_entrega_lab_1','intentos_lab_1','lab_2'])
                                                    
                # Se seleccionan los datos para predecir
                test = data.drop(['student'], axis= 1)

                # Se genera la predicción para el curso
                prediccion = rf.predict(test)

                # Se adiciona la columna: Predicción al DataFrame
                prediccion = pd.DataFrame(prediccion,columns=['prediction'])
        
                # Se concatena en el DataFrame con el estudiante y la predicción
                result= pd.concat([data['student'], prediccion], axis=1)

                # Se ordenan los valores por la columna prediccion de menor a mayor
                result = result.sort_values('prediction')

                # Se actualiza final_prediccion en la tabla calificaciones de la BD
                for i in result.index:
                    update = """ UPDATE early_intervention.classification_data SET prediction = %s 
                                 WHERE course_id = %s
                                 AND week_prediction = %s
                                 AND student = %s """
                    parametros = (str(result['prediction'][i]),
                                  curso_id,
                                  semana,
                                  result['student'][i])
                    cursor.execute(update, parametros)
        
        # Se ejecuta el query para mostrar los registros en el html
        select = (""" SELECT student, lab1, delivery_time_lab1, number_tried_lab1, 
                    result_lab1, lab2, prediction 
                    FROM early_intervention.classification_data
                    WHERE course_id = %s
                    AND week_prediction = %s
                    AND prediction <> 2
                    ORDER BY lab1 ASC """)
        parametros = (curso_id, semana)
        cursor.execute(select, parametros)
        
        result = cursor.fetchall()
        
        # Se renderiza con el Contexto con los parámetros
        context = {"datos": result, "usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'performance_classification.html', context= context)

        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Predición Clasificacion Desempeño  *****





# ***** Intervención con Mensaje *****
def intervention_message(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'intervention_message.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Intervención con Mensaje *****





# ***** Enviar Mensaje de Intervención *****
def send_intervention_message(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_curso = request.POST['cmbCurso']
        cmb_semestre = request.POST['cmbSemestre']
        curso_id = cmb_curso + "-" + cmb_semestre
        txt_fecha_intervencion = request.POST['txtFechaIntervencion']
        cmb_tema_intervencion = request.POST['cmbTemaIntervencion']
        txt_asunto = request.POST['txtAsunto']
        txt_mensaje = request.POST['txtMensaje']

        # Se definen los vectores para enviar el email de forma masiva
        email_estudiante = []
        email_prueba = []
        hoy = date.today()

        # Se consulta el email de los estudiantes cuya predicción es diferente a 2 (alto desmepeño) 
        select = (""" SELECT DISTINCT U.email
                      FROM early_intervention.classification_data AS CD, inginious.users AS U
                      WHERE CD.student = U.realname
                      AND CD.course_id = %(course_id)s
                      AND CD.prediction <> 2 """)
        cursor.execute(select, {'course_id': curso_id})

        registro = cursor.fetchall()

        # Se carga el vector (email_estudiante) con los registros de la BD
        for email in registro:
            email = str(email)
            email = email.replace("('","")
            email = email.replace("',)","")
            email_estudiante.append(email)
        
        # Se envía el email a cada estudiante
        #email_estudiante.append('jose.llanos@correounivalle.edu.co' )
        email_prueba.append('chepe159@gmail.com')

        asunto = txt_asunto
        mensaje = txt_mensaje
        email_from = 'ing.jose.llanos@gmail.com'
        email_to = email_prueba
        #reply_to = 'ing.jose.llanos@gmail.com'
        '''
        mail = EmailMessage(
            asunto,
            mensaje,
            email_from,
            email_to, 
        )
        mail.send()
        '''

        # Se guarda el registro en la tabla: intervention_message
        insert = (""" INSERT INTO early_intervention.intervention_message (course_id, 
                      intervention_date, intervention_topic,affair, message, students, date)
                      VALUES(%s, %s, %s, %s, %s, %s, %s) """)
        parametros = (curso_id, str(txt_fecha_intervencion), str(cmb_tema_intervencion), 
                      asunto, mensaje, str(email_estudiante), str(hoy))
        cursor.execute(insert, parametros)


        context = {"emails": email_estudiante, "usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'intervention_message.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Enviar Mensaje de Intervención *****


# ***** Reporte Intervención Preventiva *****
def preventive_intervention_report(request):
    # Validación de variables de sesión
    try:
        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'preventive_intervention_report.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Reporte Intervención Preventiva *****




# ***** Mostrar Reporte Intervención Preventiva *****
def show_preventive_intervention_report(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_curso = request.POST['cmbCurso']
        cmb_semestre = request.POST['cmbSemestre']
        curso_id = cmb_curso + "-" + cmb_semestre
        registros_estudiantes = []

        # Se consulta la cantidad de tutorías programadas  
        select = (""" SELECT count(*) AS contador
                      FROM early_intervention.intervention_assistance
                      WHERE course_id = %(course_id)s """)
        cursor.execute(select, {'course_id': curso_id})

        registros = cursor.fetchall()

        cantidad_tutorias = str(registros)
        cantidad_tutorias = cantidad_tutorias.replace("[(", "")
        cantidad_tutorias = cantidad_tutorias.replace(",)]","")
        cantidad_tutorias = int(cantidad_tutorias)

        # Se consulta la cantidad de asistencias por estudiante
        select = (""" SELECT iad.student, count(iad.attended)
                      FROM early_intervention.intervention_assistance AS ia, early_intervention.intervention_assistance_detail iad
                      WHERE ia.id = iad.id_intervention_assistance
                      AND ia.course_id = %(course_id)s
                      AND attended = 1
                      GROUP BY iad.student
                      ORDER BY iad.student ASC """)
        cursor.execute(select, {'course_id': curso_id})

        registros_asistencia = cursor.fetchall()

        for row_asistencia in registros_asistencia:
            estudiante = row_asistencia[0]
            contador_asistencias = row_asistencia[1]
            contador_asistencias = int(contador_asistencias)

            # Se calcula el porcentaje de asistencia a intervención
            porcentaje_asistencia = (contador_asistencias * 100) / cantidad_tutorias
            
            # Se consulta la calificación (lab1 y lab2) y predicción del estudiante
            select = (""" SELECT DISTINCT student, lab1, lab2, prediction
                          FROM early_intervention.classification_data
                          WHERE course_id = %s
                          AND student = %s
                          ORDER BY student ASC """)
            parametros = (curso_id, estudiante)
            cursor.execute(select, parametros)

            registros_calificacion = cursor.fetchall()

            for row_calificacion in registros_calificacion:
                lab1 = row_calificacion[1]
                lab2 = row_calificacion[2]
                promedio_calificacion = (lab1 + lab2) / 2
                prediccion = row_calificacion[3]
                

            # Se cargan el registro al vector
            registros_estudiantes.append([estudiante, lab1, lab2, 
                                          promedio_calificacion, prediccion,
                                          cantidad_tutorias, contador_asistencias, 
                                          round(porcentaje_asistencia,2)])

        context = {"datos": registros_estudiantes, "usuario": request.session['usuario'], "rol": request.session['rol']}
        
        # *** Plantilla ***
        return render(request, 'preventive_intervention_report.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Mostrar Reporte Intervención Preventiva *****




### ----------------------------------------------------------------------

# ***** Intervención con Sugerencia *****
def intervention_suggestion(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se ejecuta el query para mostrar los registros en el html
        cursor.execute(""" SELECT course_id, semester, suggestion, students, date
                           FROM early_intervention.intervention_suggestion """)
        result = cursor.fetchall()
        

        context = {"datos": result, "usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'intervention_suggestion.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Intervención con Sugerencia *****





# ***** Cargar Sugerencia *****
def upload_suggestion(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        actividad = request.POST['cmbActividad']

        # Se consulta la sugerencia
        select = (""" SELECT suggestion 
                      FROM early_intervention.suggestions
                      WHERE task_id = %(task_id)s """)
        cursor.execute(select, {'task_id': actividad})

        registro = cursor.fetchall()

        registro = str(registro)
        registro = registro.replace("[('", "")
        registro = registro.replace("',)]", "")

        context = {"sugerencia": registro, "usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'intervention_suggestion.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Cargar Sugerencia *****





# ***** Enviar Sugerencia de Intervención *****
def send_intervention_suggestion(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        curso = request.POST['cmbCurso']
        semestre = request.POST['cmbSemestre']
        curso_id = curso + "-" + semestre
        email_estudiante = []
        email_prueba = []
        mensaje = "--------------------------------------\n"
        mensaje += "Sugerencia/Recomendación\n"
        mensaje += "-------------------------------------\n"
        mensaje += request.POST['txtSugerencia']
        hoy = date.today()
        
        # Se consulta el valor de la predicción
        select = (""" SELECT DISTINCT U.email
                      FROM early_intervention.classification_data AS CD, inginious.users AS U
                      WHERE CD.student = U.realname
                      AND CD.course_id = %(course_id)s
                      AND CD.prediction <> 2 """)
        cursor.execute(select, {'course_id': curso_id})

        registro = cursor.fetchall()


        # Se envía el email a cada estudiante
        for email in registro:
            email = str(email)
            email = email.replace("('","")
            email = email.replace("',)","")
            email_estudiante.append(email)
        
        # Se envía el email a cada estudiante
        #email_estudiante.append('jose.llanos@correounivalle.edu.co')
        email_prueba.append('chepe159@gmail.com')

        asunto = 'Intervención Preventiva SPEI: Sugerencia/Recomendación'
        mensaje = mensaje
        email_from = 'ing.jose.llanos@gmail.com'
        email_to = email_prueba
        #reply_to = 'ing.jose.llanos@gmail.com'
        
        mail = EmailMessage(
            asunto,
            mensaje,
            email_from,
            email_to, 
        )
        mail.send()

        # Se guarda el registro en la tabla: intervention_suggestion
        insert = (""" INSERT INTO early_intervention.intervention_suggestion (course_id, semester, suggestion, students, date)
                      VALUES(%s, %s, %s, %s, %s) """)
        parametros = (curso, semestre, mensaje, str(email_estudiante), str(hoy))
        cursor.execute(insert, parametros)

        context = {"emails": email_estudiante, "usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'intervention_suggestion.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Enviar Sugerencia de Intervención *****





# ***** Intervención con Código *****
def intervention_code(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se ejecuta el query para mostrar los registros en el html
        cursor.execute(""" SELECT course_id, semester, message, code, students, date
                           FROM early_intervention.intervention_code """)
        result = cursor.fetchall()
        

        context = {"datos": result, "usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'intervention_code.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Intervención con Código *****





# ***** Cargar Código *****
def upload_code(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        actividad = request.POST['cmbActividad']
        codigo_fuente = ""

        if actividad == "Lab1-Problema1":

            # Se ejecuta el query para mostrar los registros en el html
            '''
            cursor.execute(""" SELECT code
                               FROM early_intervention.code 
                               WHERE task_id = 'Lab1-Problema1' """)

            codigo_fuente = cursor.fetchall()
            '''
            codigo_fuente += "Laboratorio 1 - Problema 1\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "1:Cabecera del archivo\n"
            codigo_fuente += "Nombre: Julian Alexander Alvarez Payares\n"
            codigo_fuente += "Correo: alvarez.julian@correounivalle.edu.co\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "2:Análisis del problema\n"
            codigo_fuente += "\n"
            codigo_fuente += "Descripción Funcionalidad:\n"
            codigo_fuente += "En una cinemateca se lleva el registro de las películas que se exhiben.\n"
            codigo_fuente += "De cada película se solicitan cinco valores, estos son: el título, el\n"
            codigo_fuente += "país de origen, el género, la duración (en minutos) y el año de estreno.\n"
            codigo_fuente += "Usted debe desarrollar un programa que permita registrar la información\n"
            codigo_fuente += "de las películas. A continuación se muestra un ejemplo de la entrada de\n"
            codigo_fuente += "\n"
            codigo_fuente += "Entradas:\n"
            codigo_fuente += "La escafandra y la mariposa\n"
            codigo_fuente += "Francia\n"
            codigo_fuente += "Drama\n"
            codigo_fuente += "112\n"
            codigo_fuente += "2007\n"
            codigo_fuente += "\n"
            codigo_fuente += "Salidas:\n"
            codigo_fuente += "DATOS DE LA PELÍCULA\n"
            codigo_fuente += "TÍTULO: La escafandra y la mariposa\n"
            codigo_fuente += "PAÍS DE ORIGEN: Francia\n"
            codigo_fuente += "GÉNERO: Drama\n"
            codigo_fuente += "DURACIÓN: 112 minutos\n"
            codigo_fuente += "AÑO DE ESTRENO: 2007\n"
            codigo_fuente += "\n"
            codigo_fuente += "Proceso: Debo crear 5 variables de tipo string,\n"
            codigo_fuente += "el nombre de cada variable es nombrePelicula, paisOrigen, genero, duración y\n"
            codigo_fuente += "fechaEstreno, respectivamente. Despues, debo agregar unos cout para imprimir el\n"
            codigo_fuente += "mensaje en pantalla como es requerido.\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "3: Algoritmo en pseudocódigo\n"
            codigo_fuente += "Inicio\n"
            codigo_fuente += "  nombrePelicula, paisOrigen, genero: cadena\n"
            codigo_fuente += "  duración y fechaEstreno: entero\n"
            codigo_fuente += "  preguntar(nombrePelicula)\n"
            codigo_fuente += "  preguntar(paisOrigen)\n"
            codigo_fuente += "  preguntar(genero)\n"
            codigo_fuente += "  preguntar(duración)\n"
            codigo_fuente += "  preguntar(fechaEstreno)\n"
            codigo_fuente += "  mostrar(nombrePelicula)\n"
            codigo_fuente += "  mostrar(paisOrigen)\n"
            codigo_fuente += "  mostrar(genero)\n"
            codigo_fuente += "  mostrar(duración)\n"
            codigo_fuente += "  mostrar(fechaEstreno)\n"
            codigo_fuente += "Fin\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "4: Pruebas de escritorio\n"
            codigo_fuente += "\n"
            codigo_fuente += "Prueba 1:\n"
            codigo_fuente += "nombrePelicula = La escafandra y la mariposa\n"
            codigo_fuente += "paisOrigen = Francia\n"
            codigo_fuente += "genero = Drama\n"
            codigo_fuente += "duración = 112\n"
            codigo_fuente += "fechaEstreno = 2007\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "//5: Algoritmo en C++, por ejemplo:\n"
            codigo_fuente += "#include <iostream>\n"
            codigo_fuente += "using namespace std;\n"
            codigo_fuente += "// Inicio\n"
            codigo_fuente += "int main() {\n"
            codigo_fuente += "  // Datos de entradas\n"
            codigo_fuente += "  string nombrePelicula, paisOrigen, genero,duracion, fechaEstreno;\n"
            codigo_fuente += "  // Preguntar el título de la película\n"
            codigo_fuente += "  cerr << 'Digite el título de la película: ';\n"
            codigo_fuente += "  //cin >> nombrePelicula;\n"
            codigo_fuente += "  getline(std::cin, nombrePelicula);\n"
            codigo_fuente += "\n"
            codigo_fuente += "  // Preguntar el país de origen\n"
            codigo_fuente += "  cerr << 'Digite el país de origen: ';\n"
            codigo_fuente += "  cin >> paisOrigen;\n"
            codigo_fuente += "  // Preguntar el género\n"
            codigo_fuente += "  cerr << 'Digite el género: ';\n"
            codigo_fuente += "  cin >> genero;\n"
            codigo_fuente += "  // Preguntar la duración\n"
            codigo_fuente += "  cerr << 'Digite la duración en minutos: ';\n"
            codigo_fuente += "  cin >> duracion;\n"
            codigo_fuente += "  // Preguntar el año de estreno\n"
            codigo_fuente += "  cerr << 'Digite el año de estreno: ';\n"
            codigo_fuente += "  cin >> fechaEstreno;\n"
            codigo_fuente += "\n"
            codigo_fuente += "  // Datos de salidas\n"
            codigo_fuente += "  cout << 'DATOS DE LA PELÍCULA' << endl;\n"
            codigo_fuente += "  cout << 'TÍTULO: ' << nombrePelicula << endl;\n"
            codigo_fuente += "  cout << 'PAÍS DE ORIGEN: ' << paisOrigen << endl;\n"
            codigo_fuente += "  cout << 'GÉNERO: ' << genero << endl;\n"
            codigo_fuente += "  cout << 'DURACIÓN: ' << duracion << 'minutos' << endl;\n"
            codigo_fuente += "  cout << 'AÑO DE ESTRENO: ' << fechaEstreno << endl;\n"
            codigo_fuente += "//Fin\n"
            codigo_fuente += "}\n"

        elif actividad == "Lab1-Problema2": 
            codigo_fuente += "Laboratorio 1 - Problema 2\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "1:Cabecera del archivo\n"
            codigo_fuente += "\n"
            codigo_fuente += "Nombre: Julian Alexander Alvarez Payares\n"
            codigo_fuente += "Correo: alvarez.julian@correounivalle.edu.co\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "2:Análisis del problema\n"
            codigo_fuente += "\n"
            codigo_fuente += "Descripción Funcionalidad:\n"
            codigo_fuente += "En un almacén que se dedica a la venta de teléfonos inteligentes se quiere\n"
            codigo_fuente += "conocer el IVA, el costo, y la ganancia neta de sus productos. Estos tres\n"
            codigo_fuente += "rubros corresponden al 19%, 61%, y 20%, respectivamente, y se calculan sobre\n"
            codigo_fuente += "el valor del producto. Usted debe desarrollar un programa que permita calcular\n"
            codigo_fuente += "los valores requeridos por el almacén. El programa debe inicialmente solicitar\n"
            codigo_fuente += "dos valores, el nombre y el precio del producto. Luego, se muestran cuatro\n"
            codigo_fuente += "datos, el nombre, el IVA, el costo, y la ganancia neta. A continuación se\n"
            codigo_fuente += "muestra un ejemplo de la entrada de datos:\n"
            codigo_fuente += "\n"
            codigo_fuente += "Entradas:\n"
            codigo_fuente += "Samsung Galaxy A31\n"
            codigo_fuente += "729900\n"
            codigo_fuente += "\n"
            codigo_fuente += "Salidas:\n"
            codigo_fuente += "\n"
            codigo_fuente += "Producto: Samsung Galaxy A31\n"
            codigo_fuente += "IVA: 138681\n"
            codigo_fuente += "Costo: 445239\n"
            codigo_fuente += "Ganancia Neta: 145980\n"
            codigo_fuente += "\n"
            codigo_fuente += "Proceso: Debo crear 2 variables, una de tipo string y la otra de tipo entero,\n"
            codigo_fuente += "para recibir el nombre del producto y el precio del mismo, despues con el valor\n"
            codigo_fuente += "del precio debo crear 3 variables de tipo entero para calcular el precio del\n"
            codigo_fuente += "iva que es del 19%, despues calcular el costo que es el 61% y por ultimo la\n"
            codigo_fuente += "ganancia que es del 20%, ultimamente\n"
            codigo_fuente += "muestro los datos.\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "3: Algoritmo en pseudocódigo\n"
            codigo_fuente += "\n"
            codigo_fuente += "Inicio\n"
            codigo_fuente += "  nombreProducto: cadena;\n"
            codigo_fuente += "  precioProducto, IVA, costo, gananciaNeta: entero;\n"
            codigo_fuente += "\n"
            codigo_fuente += "  preguntar(nombreProducto)\n"
            codigo_fuente += "  preguntar(precio)\n"
            codigo_fuente += "\n"
            codigo_fuente += "  IVA = (precioProducto * 19)/100\n"
            codigo_fuente += "  costo = (precioProducto * 61)/100\n"
            codigo_fuente += "  gananciaNeta = (precioProducto * 20)/100\n"
            codigo_fuente += "\n"
            codigo_fuente += "  mostrar(nombreProducto)\n"
            codigo_fuente += "  mostrar(IVA)\n"
            codigo_fuente += "  mostrar(costo)\n"
            codigo_fuente += "  mostrar(gananciaNeta)\n"
            codigo_fuente += "\n"
            codigo_fuente += "Fin\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "4: Pruebas de escritorio\n"
            codigo_fuente += "\n"
            codigo_fuente += "Prueba 1:\n"
            codigo_fuente += "nombreProducto = Samsung Galaxy A31\n"
            codigo_fuente += "precioProducto = 729900\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "//5. Algoritmo en C++:\n"
            codigo_fuente += "#include <iostream>\n"
            codigo_fuente += "using namespace  std;\n"
            codigo_fuente += "\n"
            codigo_fuente += "// Inicio\n"
            codigo_fuente += "int main() {\n"
            codigo_fuente += "//***Entradas***\n"
            codigo_fuente += "cerr << 'Digite el nombre del producto: ';\n"
            codigo_fuente += "getline (cin,nombreProducto);\n"
            codigo_fuente += "cerr << 'Digite el precio del producto: ';\n"
            codigo_fuente += "cin >> precioProducto;\n"
            codigo_fuente += "//*** Proceso ***\n"
            codigo_fuente += "valorIva = precioProducto * 0.19;\n"
            codigo_fuente += "valorCosto = precioProducto * 0.61;\n"
            codigo_fuente += "valorNeto = precioProducto * 0.20;\n"
            codigo_fuente += "// *** Salida ***\n"
            codigo_fuente += "cout << 'Producto: ' << nombreProducto << endl;\n"
            codigo_fuente += "cout << 'IVA: ' << valorIva << endl;\n"
            codigo_fuente += "cout << 'Costo: ' << valorCosto endl;\n"
            codigo_fuente += "cout << 'Ganancia Neta: ' << valorNeto << endl;\n"
            codigo_fuente += "}\n"

        elif actividad == "Lab2-Problema1": 
            codigo_fuente += "Laboratorio 2 - Problema 1\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "Nombre:Jose Miguel Llanos\n"
            codigo_fuente += "Mail:jose.llanos@correounivalle.edu.co\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "/*analisis\n"
            codigo_fuente += "Entradas:\n"
            codigo_fuente += "nombre : texto\n"
            codigo_fuente += "peso : real\n"
            codigo_fuente += "altura : real\n"
            codigo_fuente += "Salidas:\n"
            codigo_fuente += "nombre : texto\n"
            codigo_fuente += "IMC : real\n"
            codigo_fuente += "categoria : texto\n"
            codigo_fuente += "Proceso:Calcular el IMC del paciente y con base en este determinar su categoria.\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "/*Pseudocodigo\n"
            codigo_fuente += "Inicio\n"
            codigo_fuente += "   nombre    : cadena\n"
            codigo_fuente += "   peso      : real\n"
            codigo_fuente += "   altura    : real\n"
            codigo_fuente += "   IMC       : real\n"
            codigo_fuente += "   categoria : texto\n"
            codigo_fuente += "   // Entradas\n"
            codigo_fuente += "   preguntar(nombre)\n"
            codigo_fuente += "   preguntar(peso)\n"
            codigo_fuente += "   preguntar(altura)\n"
            codigo_fuente += "   // Proceso\n"
            codigo_fuente += "   IMC = peso/(altura*altura)\n"
            codigo_fuente += "   // Salidas\n"
            codigo_fuente += "   si IMC<18.5 entonces\n"
            codigo_fuente += "      categoria = 'Infrapeso'\n"
            codigo_fuente += "      mostrar(nombre)\n"
            codigo_fuente += "      mostrar(IMC)\n"
            codigo_fuente += "      mostrar(categoria)\n"
            codigo_fuente += "   si IMC>=18.5 y IMC<25.0 entonces\n"
            codigo_fuente += "      categoria = 'Normal'\n"
            codigo_fuente += "     mostrar(nombre)\n"
            codigo_fuente += "      mostrar(IMC)\n"
            codigo_fuente += "      mostrar(categoria)\n"
            codigo_fuente += "   si IMC>=25.0 entonces\n"
            codigo_fuente += "      categoria = 'Sobrepeso'\n"
            codigo_fuente += "      mostrar(nombre)\n"
            codigo_fuente += "      mostrar(IMC)\n"
            codigo_fuente += "      mostrar(categoria)\n"    
            codigo_fuente += "Fin\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "/*Pruebas de escritorio\n"
            codigo_fuente += "Nombre         Peso  Altura  PACIENTE       IMC      Categoria\n"
            codigo_fuente += "Alex Valencia  68.3  1.72    Alex Valencia  23.0868  Normal\n"
            codigo_fuente += "María Caicedo  55.1  1.62    María Caicedo  20.9953  Normal\n"
            codigo_fuente += "Juan Morales   90.1  1.71    Juan Morales   30.8129  Sobrepeso\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "\n"
            codigo_fuente += "//Código en C++\n"
            codigo_fuente += "int main() {\n"
            codigo_fuente += "#include <iostream>\n"
            codigo_fuente += "using namespace  std;\n"
            codigo_fuente += "\n"
            codigo_fuente += "// Inicio\n"
            codigo_fuente += "int main() {\n"
            codigo_fuente += "//nombre, categoria : cadena\n"
            codigo_fuente += "string nombre, categoria;\n"
            codigo_fuente += "//peso, altura, IMC : real\n"
            codigo_fuente += "float peso, altura, IMC;\n"
            codigo_fuente += "//preguntar(nombre)\n"
            codigo_fuente += "cerr << 'Digite el nombre: ';\n"
            codigo_fuente += "getline(cin, nombre);\n"
            codigo_fuente += "//preguntar(peso)\n"
            codigo_fuente += "cerr << 'Digite el peso: ';\n"
            codigo_fuente += "cin >> peso;\n"
            codigo_fuente += "//preguntar(altura)\n"
            codigo_fuente += "cerr << 'Digite la altura: ';\n"
            codigo_fuente += "cin >> altura;\n"
            codigo_fuente += "// IMC = peso/(altura*altura)\n"
            codigo_fuente += "IMC = peso / (altura * altura);\n"
            codigo_fuente += "if(IMC < 18.5){\n"
            codigo_fuente += " categoria = 'Infrapeso';\n"
            codigo_fuente += " cout << 'PACIENTE: ' << nombre << endl;\n"
            codigo_fuente += " cout << 'IMC: ' << IMC << endl;\n"
            codigo_fuente += " cout << 'Categoria: ' << categoria << endl;\n"
            codigo_fuente += "}\n"
            codigo_fuente += "if(IMC >= 18.5 && IMC < 25.0){\n"
            codigo_fuente += " categoria = 'Normal';\n"
            codigo_fuente += " cout << 'PACIENTE: ' << nombre << endl;\n"
            codigo_fuente += " cout << 'IMC: ' << IMC << endl;\n"
            codigo_fuente += " cout << 'Categoria: ' << categoria << endl;\n"
            codigo_fuente += "}\n"
            codigo_fuente += "if(IMC >= 25.0){\n"
            codigo_fuente += " categoria = 'Sobrepeso';\n"
            codigo_fuente += " cout << 'PACIENTE: ' << nombre << endl;\n"
            codigo_fuente += " cout << 'IMC: ' << IMC << endl;\n"
            codigo_fuente += " cout << 'Categoria: ' << categoria << endl;\n"
            codigo_fuente += "}\n"

        elif actividad == "Lab2-Problema2": 
            codigo_fuente += "Laboratorio 2 - Problema 2\n"
            codigo_fuente += "/*\n"
            codigo_fuente += "Nombre: Jose Llanos\n"
            codigo_fuente += "Mail: jose.llanos@correounivalle.edu.co\n"
            codigo_fuente += "\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "/*analisis\n"
            codigo_fuente += "Entradas:\n"
            codigo_fuente += "x : entero\n"
            codigo_fuente += "Salidas:\n"
            codigo_fuente += "Fx : entero\n"
            codigo_fuente += "Proceso:Calcular el valor de f(x) dado un valor x.\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "/*Pseudocodigo\n"
            codigo_fuente += "Inicio CalculcarFx(x)\n"
            codigo_fuente += "   Fx : entero\n"
            codigo_fuente += "    si (x<=0)\n"
            codigo_fuente += "        Fx=8*(x*x)-6;\n"
            codigo_fuente += "        mostrar ('f('x') = 'Fx)\n"
            codigo_fuente += "   si (x>0)\n"
            codigo_fuente += "      Fx=3*(x)+5;\n"
            codigo_fuente += "        mostrar ('f('x') = 'Fx)\n"
            codigo_fuente += "   retornar(Fx)\n"
            codigo_fuente += "Fin\n"
            codigo_fuente += "Inicio main()\n"
            codigo_fuente += "   x : entero\n"
            codigo_fuente += "   fx :  entero\n"
            codigo_fuente += "   preguntar (x)\n"
            codigo_fuente += "   si x<=0 entonces\n"
            codigo_fuente += "      fx = 8*(x*x)-6\n"
            codigo_fuente += "      mostrar(fx)\n"
            codigo_fuente += "   si (x>0)\n"
            codigo_fuente += "      fx =3*(x)+5\n"
            codigo_fuente += "      mostrar(fx)\n"
            codigo_fuente += "Fin\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "/*Pruebas de escritorio\n"
            codigo_fuente += "x     f(x)\n"
            codigo_fuente += "10    35\n"
            codigo_fuente += "-7    386\n"
            codigo_fuente += "0     -6\n"
            codigo_fuente += "*/\n"
            codigo_fuente += "//Código en C++\n"
            codigo_fuente += "int main() {\n"
            codigo_fuente += "#include <iostream>\n"
            codigo_fuente += "using namespace  std;\n"
            codigo_fuente += "\n"
            codigo_fuente += "// Inicio\n"
            codigo_fuente += "int main() {\n"
            codigo_fuente += "int x, fx;\n"
            codigo_fuente += "\n"
            codigo_fuente += "cerr << 'Digite el valor de x: ';\n"
            codigo_fuente += "cin >> x;\n"
            codigo_fuente += "\n"
            codigo_fuente += " if(x<=0){\n"
            codigo_fuente += "    fx = 8*(x*x)-6;\n"
            codigo_fuente += "    cout << 'f(x) = ' << fx<<endl;\n"
            codigo_fuente += "  }\n"
            codigo_fuente += " if(x>0){\n"
            codigo_fuente += "    fx = 3*(x)+5;\n"
            codigo_fuente += "    cout << 'f(x) = ' << fx<<endl;\n"
            codigo_fuente += " }\n"
            codigo_fuente += "}\n"

        context = {"actividad": actividad,"codigo": codigo_fuente, "usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'intervention_code.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Cargar Código  *****






# ***** Enviar Código de Intervención *****
def send_intervention_code(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        curso = request.POST['cmbCurso']
        semestre = request.POST['cmbSemestre']
        curso_id = curso + "-" + semestre
        email_estudiante = []
        email_prueba = []
        hoy = date.today()

        # Se consulta el valor de la predicción
        select = (""" SELECT DISTINCT U.email
                      FROM early_intervention.classification_data AS CD, inginious.users AS U
                      WHERE CD.student = U.realname
                      AND CD.course_id = %(course_id)s
                      AND CD.prediction <> 2 """)
        cursor.execute(select, {'course_id': curso_id})

        registro = cursor.fetchall()


        # Se envía el email a cada estudiante
        for email in registro:
            email = str(email)
            email = email.replace("('","")
            email = email.replace("',)","")
            email_estudiante.append(email)
        
        # Se envía el email a cada estudiante
        #email_estudiante.append('jose.llanos@correounivalle.edu.co')
        email_prueba.append('chepe159@gmail.com')

        asunto = 'Intervención Preventiva SPEI: Código Fuente Referencia'
        mensaje = request.POST['txtMensaje']
        email_from = 'ing.jose.llanos@gmail.com'
        email_to = email_prueba
        #reply_to = 'ing.jose.llanos@gmail.com'
        
        mail = EmailMessage(
            asunto,
            mensaje,
            email_from,
            email_to, 
        )
        mail.attach_file('SPEI/data/lab1-p1.cpp')
        mail.attach_file('SPEI/data/lab1-p2.cpp')
        mail.attach_file('SPEI/data/lab2-p1.cpp')
        mail.attach_file('SPEI/data/lab2-p2.cpp')
        mail.send()

        # Se guarda el registro en la tabla: intervention_suggestion
        insert = (""" INSERT INTO early_intervention.intervention_code (course_id, semester, message, code, students, date)
                      VALUES(%s, %s, %s, %s, %s, %s) """)
        parametros = (curso, semestre, str(mensaje), request.POST['txtCodigo'], str(email_estudiante), str(hoy))
        cursor.execute(insert, parametros)

        context = {"emails": email_estudiante, "usuario": request.session['usuario'], "rol": request.session['rol']}
        
        # *** Plantilla ***
        return render(request, 'intervention_code.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Enviar Código de Intervención *****


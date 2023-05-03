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

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql



# ***** Clasificación Desempeño Estudiante *****
def performance_classification(request):
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

        # Se consulta la semana de intervención
        cursor.execute(""" SELECT week 
                           FROM early_intervention.intervention_week
                           WHERE week <> 7
                           AND state = 'A' """)
        intervention_week = cursor.fetchall()

        context = {"course":            course,
                   "semester":          semester, 
                   "intervention_week": intervention_week,
                   "user":              request.session['user'], 
                   "role":              request.session['role']}
        
        # *** Plantilla ***
        return render(request, 'preventive_intervention/performance_classification.html', context= context)
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
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        week = request.POST['cmbInterventionWeek']

        # Se cargan los datos de entrenamiento para el modelo de clasificación
        data = pd.read_csv("SPEI/data/entrenamiento_clasificacion_468.csv", sep=';')

        # Se limpian los datos
        data = data.dropna()

        # Se realiza el resample de los datos
        from sklearn.utils import resample
        

        # 189
        #df_bajo = data[data['Grade2'] == 0]
        #df_medio = data[data['Grade2'] == 1]
        #df_alto = data[data['Grade2'] == 2]

        #data_resample_medio = resample(df_medio,
        #                replace = True,
        #                n_samples = 101,
        #                random_state = 1)

        #data_resample_alto = resample(df_alto,
        #                replace = True,
        #                n_samples = 101,
        #                random_state = 1)

        #data2 = pd.concat([df_bajo, data_resample_medio, data_resample_alto])


        # 468
        df_low = data[data['grade'] == 0]
        df_half = data[data['grade'] == 1]
        df_high = data[data['grade'] == 2]

        df_low = data[data['grade'] == 0]
        df_half = data[data['grade'] == 1]
        df_high = data[data['grade'] == 2]

        data_resample_low = resample(df_low,
                        replace = True,
                        n_samples = 200,
                        random_state = 1)

        data_resample_high = resample(df_high,
                        replace = True,
                        n_samples = 200,
                        random_state = 1)

        data2 = pd.concat([data_resample_low, df_half, data_resample_high])

        # Se seleccionan las características según la semana
        if week == '3':
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
        #print(classification_report(y_test, pred))

        
        ### -----------------------------------------------
        # Ejemplo Predicción
        #lab1 = [5.0, 5.0, 0.0, 5.0, 5.0, 0.0]
        #tiempo_entrega = [10.24, 20.18, 0.00, 12.96, 15.91, 9.11]
        #cantidad_intentos = [4, 4, 0, 4, 4, 4]
        #tipo_matricula = [1, 1, 0, 1, 1, 1]
        
        #lab1 = [5.0, 5.0, 5.0, 5.0]
        #tiempo_entrega = [0.5, 0.70, 1.45, 7.04]
        #cantidad_intentos = [5, 5, 5, 5]
        #tipo_matricula = [1, 1, 1, 1]


        #y = pd.DataFrame({'Laboratorio-1': lab1, 'Tiempo-Entrega-Lab1': tiempo_entrega, 
        #                'Cantidad-Intentos-Lab1': cantidad_intentos, 'Tipo-Matricula': tipo_matricula})

        #x = rf.predict(y)

        #print("Predicción: Desempeño Estudiante RFC = ", x)
        ### -----------------------------------------------


        # Se consulta el id de courses_semesters
        select = (""" SELECT id 
                      FROM early_intervention.courses_semesters 
                      WHERE id_course = %s
                      AND id_semester = %s
                      AND state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Se consulta el valor de la predicción
        select = (""" SELECT prediction 
                      FROM early_intervention.classification_data
                      WHERE id_courses_semesters = %s 
                      AND week_prediction = %s """)
        parameter = (id_courses_semesters[0], week)
        cursor.execute(select, parameter)
        prediction = cursor.fetchone()

        # Si predicción es igual a -1, entonces se realiza la predicción
        if prediction[0] == -1 :
            # se selecciona la semana a predecir
            # Si la semana es igual a 3
            if week == '3':
                # Se cargan los registros 
                select = (""" SELECT student, lab1, delivery_time_lab1, number_tried_lab1
                              FROM early_intervention.classification_data
                              WHERE id_courses_semesters = %s 
                              AND week_prediction = %s """)
                parameter = (id_courses_semesters[0], week)
                cursor.execute(select, parameter)
                record = cursor.fetchall()
                
                # Se cargan los registros en un DataFrame
                data = pd.DataFrame(record, 
                                    columns=['student',
                                             'lab_1',
                                             'tiempo_entrega_lab_1',
                                             'intentos_lab_1'])
                                                    
                # Se seleccionan los datos para predecir
                test = data.drop(['student'], axis= 1)

                # Se genera la predicción para el curso
                prediction = rf.predict(test)

                # Se adiciona la columna: Predicción al DataFrame
                prediction = pd.DataFrame(prediction,columns=['prediction'])
        
                # Se concatena en el DataFrame con el estudiante y la predicción
                result= pd.concat([data['student'], prediction], axis=1)

                # Se ordenan los valores por la columna prediccion de menor a mayor
                result = result.sort_values('prediction')

                # Se actualiza final_prediction en la tabla calificaciones de la BD
                for i in result.index:
                    update = """ UPDATE early_intervention.classification_data 
                                 SET prediction = %s 
                                 WHERE id_courses_semesters = %s
                                 AND week_prediction = %s
                                 AND student = %s """
                    parameter = (str(result['prediction'][i]),
                                 id_courses_semesters[0],
                                 week,
                                 result['student'][i])
                    cursor.execute(update, parameter)

            # Sino la semana es igual a 5
            else:
                # Se cargan los registros 
                select = (""" SELECT student, lab1, delivery_time_lab1, number_tried_lab1, lab2
                              FROM early_intervention.classification_data
                              WHERE id_courses_semesters = %s 
                              AND week_prediction = %s """)
                parameter = (id_courses_semesters[0], week)
                cursor.execute(select, parameter)
                record = cursor.fetchall()
                
                # Se cargan los registros en un DataFrame
                data = pd.DataFrame(record, 
                                    columns=['student',
                                             'lab_1',
                                             'tiempo_entrega_lab_1',
                                             'intentos_lab_1',
                                             'lab_2'])
                                                    
                # Se seleccionan los datos para predecir
                test = data.drop(['student'], axis= 1)

                # Se genera la predicción para el curso
                prediction = rf.predict(test)

                # Se adiciona la columna: Predicción al DataFrame
                prediction = pd.DataFrame(prediction,columns=['prediction'])
        
                # Se concatena en el DataFrame con el estudiante y la predicción
                result= pd.concat([data['student'], prediction], axis=1)

                # Se ordenan los valores por la columna prediccion de menor a mayor
                result = result.sort_values('prediction')

                # Se actualiza final_prediccion en la tabla calificaciones de la BD
                for i in result.index:
                    update = """ UPDATE early_intervention.classification_data SET prediction = %s 
                                 WHERE id_courses_semesters = %s
                                 AND week_prediction = %s
                                 AND student = %s """
                    parametros = (str(result['prediction'][i]),
                                  id_courses_semesters[0],
                                  week,
                                  result['student'][i])
                    cursor.execute(update, parametros)
        
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

        # Se consulta la semana de intervención
        cursor.execute(""" SELECT week 
                           FROM early_intervention.intervention_week
                           WHERE week <> 7
                           AND state = 'A' """)
        intervention_week = cursor.fetchall()
        
        # Se ejecuta el query para mostrar los registros en el html
        select = (""" SELECT student, lab1, delivery_time_lab1, number_tried_lab1, 
                      result_lab1, lab2, prediction 
                      FROM early_intervention.classification_data
                      WHERE id_courses_semesters = %s
                      AND week_prediction = %s
                      AND prediction <> 2
                      ORDER BY lab1 ASC """)
        parameter = (id_courses_semesters[0], week)
        cursor.execute(select, parameter)
        record = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros
        context = {"course":            course,
                   "semester":          semester,
                   "intervention_week": intervention_week, 
                   "record":            record, 
                   "user":              request.session['user'], 
                   "role":              request.session['role']}

        # *** Plantilla ***
        return render(request, 'preventive_intervention/performance_classification.html', context= context)

        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Predición Clasificacion Desempeño  *****
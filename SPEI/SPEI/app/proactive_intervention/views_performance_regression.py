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


# ***** Regresión del Desempeño del estudiante *****
def performance_regression(request):
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

        context = {"course":            course,
                   "semester":          semester, 
                   "user":              request.session['user'], 
                   "role":              request.session['role']}
        
        # *** Plantilla ***
        return render(request, 'proactive_intervention/performance_regression.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Regresión del Desempeño del estudiante *****


# ***** Predicción Regressión Desempeño *****
def performance_regression_prediction(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']

        '''
        # Se cargan los datos
        data = pd.read_csv("SPEI/data/entrenamiento_regresion_468.csv", sep=';')

        # Se limpian los datos
        data = data.dropna()

        # Selección de características y clase
        features = ['lab_1','tiempo_entrega_lab_1','intentos_lab_1','lab_2','lab_3']
        X = data[features] 
        y = data['grade']

        # Se particionan los datos
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=1)

        # ***** Modelo GBR *****
        # Se crea el modelo
        GBR =GradientBoostingRegressor(loss='huber', n_estimators=200).fit(X_train, y_train)

        predictGBR = GBR.predict(X = X_test)

        # Métricas: R2, RMSE, MAE
        #R2
        r2GBR = r2_score(y_test, predictGBR)

        #RMSE
        rmsGBR = mean_squared_error(y_test, predictGBR)

        #MAE
        maeGBR = mean_absolute_error(y_test, predictGBR)

        #print("R2 = ", round(r2GBR,2))
        #print("RMSE = ", round(rmsGBR,2))
        #print("MAE = ", round(maeGBR,2))

        ### -----------------------------------------------
        '''

        # Se cargan los datos de entrenamiento para el modelo de clasificación
        data = pd.read_csv("SPEI/data/entrenamiento_clasificacion_468.csv", sep=';')

        # Se limpian los datos
        data = data.dropna()

        # Se realiza el resample de los datos
        from sklearn.utils import resample

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
     
        # Selección de características y clase para la semana 7
        features = ['lab_1','tiempo_entrega_lab_1','intentos_lab_1','lab_2','lab_3']
        X = data2[features] 
        y = data2['grade'].values

        # Se dividen los datos para el entrenamiento (80% entrenamiento y 20% pruebas)
        X_train, X_test, y_train, y_test = train_test_split(X, y, 
                                                            train_size = 0.8, 
                                                            random_state= 1)

        # Se crea el modelo 
        rf = RandomForestClassifier(bootstrap=False, max_depth=100, min_samples_split=10)
        
        # Se entrena el modelo
        rf.fit(X_train, y_train)

        pred = rf.predict(X_test)
        
        # Se consulta el id de courses_semesters
        select = (""" SELECT id 
                      FROM early_intervention.courses_semesters 
                      WHERE id_course = %s
                      AND id_semester = %s
                      AND state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

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

        
        # Se ejecuta el query para mostrar los registros en el html
        select = (""" SELECT student, lab1, delivery_time_lab1, number_tried_lab1, lab2, lab3, average, final_prediction 
                      FROM early_intervention.regression_data
                      WHERE id_courses_semesters = %(id_courses_semesters)s
                      AND final_prediction < 4.1
                      ORDER BY lab1 ASC """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
        record = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros
        context = {"course":            course,
                   "semester":          semester,
                   "record":            record, 
                   "user":              request.session['user'], 
                   "role":              request.session['role']}

        # *** Plantilla ***
        return render(request, 'proactive_intervention/performance_regression.html', context=context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión 
# ***** Fin Predicción Regressión Desempeño ***** 
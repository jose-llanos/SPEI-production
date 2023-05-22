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

# libreria para en entrenamiento y las pruebas
from sklearn.model_selection import train_test_split
# Se importa la libreria de Gradient Boosting
from sklearn.ensemble import GradientBoostingRegressor
# librería para las métricas del modelo de regresión
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
#from sklearn.metrics import explained_variance_score

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
       
        # Se consulta el id de courses_semesters
        select = (""" SELECT id 
                      FROM early_intervention.courses_semesters 
                      WHERE id_course = %s
                      AND id_semester = %s
                      AND state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Se valida si el promedio de final_prediccion es igual o mayor a cero
        select = (""" SELECT avg(final_prediction) 
                      FROM early_intervention.regression_data 
                      WHERE id_courses_semesters = %(id_courses_semesters)s """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
        average = cursor.fetchone()

        # Si promedio es igual a 0, entonces se realiza la predicción
        if average[0] == 0 :
            # Se cargan los registros 
            select = (""" SELECT * 
                          FROM early_intervention.regression_data 
                          WHERE id_courses_semesters = %(id_courses_semesters)s """)
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            record = cursor.fetchall()

            # Se cargan los registros en un DataFrame
            data = pd.DataFrame(record, 
                                columns=['id',
                                         'semester', 
                                         'student', 
                                         'lab1', 
                                         'delivery_time_lab1', 
                                         'number_tried_lab1', 
                                         'lab2', 
                                         'lab3', 
                                         'average', 
                                         'final_prediction'])
                                         
            # Se limpian los datos
            test = data.dropna()

            # Se eliminan las columnas código y nombre del DataFrame
            test = test.drop(['id','semester','student','average','final_prediction'], axis=1)

            # Se genera la predicción para el curso
            pred_test = GBR.predict(test)
            # Se redondea la calificación a un decimal
            pred_test = np.round(pred_test, 1)

            # Se adiciona la columna: Nota_Final_Predicción al DataFrame
            final_predic = pd.DataFrame(pred_test,columns=['final_prediction'])

            # Se concatena en el DataFrame: el nombre del estudiante, las calificaciones y la nota final
            result= pd.concat([data['student'], test, final_predic], axis=1)

            # Se ordena la calificación final de la predicción de menor a mayor
            result = result.sort_values('final_prediction')

            # Se actualiza final_prediccion en la tabla calificaciones de la BD
            for i in result.index:
                update = """ UPDATE early_intervention.regression_data 
                             SET final_prediction = %s 
                             WHERE id_courses_semesters = %s
                             AND student = %s """
                parameter = (str(result['final_prediction'][i]),
                             str(id_courses_semesters[0]), 
                             str(result['student'][i]))
                cursor.execute(update, parameter)

            # Se convierte el DataFrame a una lista
            #result = result.to_numpy().tolist()
        
        # Se ejecuta el query 
        select = (""" SELECT student, lab1, delivery_time_lab1,
                      number_tried_lab1, lab2, lab3,
                      average, final_prediction
                      FROM early_intervention.regression_data  
                      WHERE id_courses_semesters = %(id_courses_semesters)s 
                      ORDER BY final_prediction ASC """)
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
        context = {"course":   course,
                   "semester": semester, 
                   "record":   record, 
                   "user":     request.session['user'], 
                   "role":     request.session['role']}

        # *** Plantilla ***
        return render(request, 'proactive_intervention/performance_regression.html', context=context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión 
# ***** Fin Predicción Regressión Desempeño ***** 
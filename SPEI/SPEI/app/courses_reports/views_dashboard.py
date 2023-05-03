# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de tiempo
import datetime

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql


# ***** Calificación actividad *****
def activity_grades(request):    
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        # Se consultan las tareas para el curso
        cursor.execute(""" SELECT DISTINCT taskid
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') 
                           AND taskid IN ('Lab1-Problema1', 'Lab1-Problema2', 'Lab2-Problema1','lab2-Problema2',
			                              'Lab3-Problema1','Lab3-Problema2','Laboratorio4','Parcial1','Parcial2')
                           ORDER BY taskid ASC """)
        task = cursor.fetchall()


        context = {"course":   course,
                   "task":     task,
                   "user":     request.session['user'], 
                   "role":     request.session['role']}
    
        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_activity_grades.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin calificación actividad *****



# ***** Visualización calificacion actividad  *****
def display_grades_activity(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        course = request.POST['cmbCourse']
        task = request.POST['cmbTask']

        # Se ejecuta el query 
        select = (""" SELECT username, grade 
                      FROM inginious.user_tasks 
                      WHERE course_id = %s 
                      AND taskid = %s
                      ORDER BY grade DESC """)
        parameter = (course, task)
        cursor.execute(select, parameter)

        # Se cargan los registros del cursos
        record = cursor.fetchall()
        
        # Se definen los vectores para los elementos del reporte
        username = []
        grade = []

        for row in record:
            username.append(row[0])
            grade.append(float(row[1]))

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        # Se consultan las tareas para el curso
        cursor.execute(""" SELECT DISTINCT taskid
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') 
                           AND taskid IN ('Lab1-Problema1', 'Lab1-Problema2', 'Lab2-Problema1','lab2-Problema2',
			                              'Lab3-Problema1','Lab3-Problema2','Laboratorio4','Parcial1','Parcial2')
                           ORDER BY taskid ASC """)
        task = cursor.fetchall()

        # Se renderiza el Contexto con los parámetros
        context = {"course": course,
                   "task":   task,
                   "name":   username, 
                   "grade":  grade, 
                   "user":   request.session['user'], 
                   "role":   request.session['role']}

        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_activity_grades.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin visualización calificacion actividad  *****



# ***** Gráfica promedio calificación *****

def average_grade(request):    
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        context = {"course":  course,
                   "user": request.session['user'], 
                   "role":     request.session['role']}
    
        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_average_grade.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin promedio calificación *****



# ***** Visualización promedio calificacion *****
def display_average_grade(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        course = request.POST['cmbCourse']
        
        # Se ejecuta el query 
        select = (""" SELECT username, AVG(grade) AS grade
                      FROM inginious.user_tasks
                      WHERE course_id = %(course)s
                      GROUP BY username
                      ORDER BY grade DESC """)
        cursor.execute(select,{'course': course})

        # Se cargan los registros del cursos
        registros = cursor.fetchall()
        
        # Se definen los vectores para los elementos del reporte
        username = []
        grade = []

        for row in registros:
            username.append(row[0])
            grade.append(float(row[1]))

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        # Se renderiza el Contexto con los parámetros
        context = {"course": course,
                   "name":   username, 
                   "grade":  grade, 
                   "user":   request.session['usuario'], 
                   "role":   request.session['rol']}

        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_average_grade.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin visualización promedio calificacion  *****



# ***** Gráfica actividades entregadas *****
def delivered_activities(request):    
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        context = {"course": course,
                   "user":   request.session['user'], 
                   "role":   request.session['role']}
    
        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_delivered_activities.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin actividades entregadas *****



# ***** Visualización actividades entregadas *****
def display_delivered_activities(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        course = request.POST['cmbCourse']

        # Se ejecuta el query 
        select = (""" SELECT username, COUNT(taskid) AS task
                      FROM inginious.user_tasks
                      WHERE course_id = %(course)s
                      GROUP BY username
                      ORDER BY task DESC """)
        cursor.execute(select,{'course': course})

        # Se cargan los registros del cursos
        record = cursor.fetchall()
        
        # Se definen los vectores para los elementos del reporte
        username = []
        task = []

        for row in record:
            username.append(row[0])
            task.append(float(row[1]))

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        # Se renderiza el Contexto con los parámetros
        context = {"course": course,
                   "name":   username, 
                   "task":   task, 
                   "user":   request.session['user'], 
                   "role":   request.session['role']}

        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_delivered_activities.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin visualización actividades entregadas  *****



# ***** Gráfica intentos actividad *****
def tried_activities(request):    
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        # Se consultan las tareas para el curso
        cursor.execute(""" SELECT DISTINCT taskid
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') 
                           AND taskid IN ('Lab1-Problema1', 'Lab1-Problema2', 'Lab2-Problema1','lab2-Problema2',
			                              'Lab3-Problema1','Lab3-Problema2','Laboratorio4','Parcial1','Parcial2')
                           ORDER BY taskid ASC """)
        task = cursor.fetchall()

        context = {"course": course,
                   "task":   task,
                   "user":   request.session['user'], 
                   "role":   request.session['role']}
    
        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_tried_activities.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin intentos actividad *****



# ***** Visualización intentos actividad  *****
def display_tried_activities(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        course = request.POST['cmbCourse']
        task = request.POST['cmbTask']

        # Se ejecuta el query 
        select = (""" SELECT username, SUM(tried) AS intentos
                      FROM inginious.user_tasks
                      WHERE course_id = %s
                      AND taskid = %s
                      GROUP BY username
                      ORDER BY intentos DESC """)
        parametros = (course, task)
        cursor.execute(select, parametros)
        record = cursor.fetchall()
        
        # Se definen los vectores para los elementos del reporte
        username = []
        tried = []

        for row in record:
            username.append(row[0])
            tried.append(float(row[1]))
        
        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        # Se consultan las tareas para el curso
        cursor.execute(""" SELECT DISTINCT taskid
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') 
                           AND taskid IN ('Lab1-Problema1', 'Lab1-Problema2', 'Lab2-Problema1','lab2-Problema2',
			                              'Lab3-Problema1','Lab3-Problema2','Laboratorio4','Parcial1','Parcial2')
                           ORDER BY taskid ASC """)
        task = cursor.fetchall()

        # Se renderiza el Contexto con los parámetros
        context = {"course": course,
                   "task":   task, 
                   "name":   username, 
                   "tried":  tried, 
                   "user":   request.session['user'], 
                   "role":   request.session['role']}

        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_tried_activities.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin visualización intentos actividad  *****



# ***** Gráfica total intentos *****
def total_tried(request):    
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        context = {"course": course,
                   "user": request.session['user'], 
                   "role": request.session['role']}
    
        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_total_tried.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin total intentos *****



# ***** Visualización total intentos *****
def display_total_tried(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        course = request.POST['cmbCourse']

        # Se ejecuta el query 
        select = (""" SELECT username, SUM(tried) AS intentos
                      FROM inginious.user_tasks
                      WHERE course_id = %(course)s
                      GROUP BY username
                      ORDER BY intentos DESC """)
        cursor.execute(select,{'course': course})
        record = cursor.fetchall()
        
        # Se definen los vectores para los elementos del reporte
        username = []
        tried = []

        for row in record:
            username.append(row[0])
            tried.append(float(row[1]))

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        # Se renderiza el Contexto con los parámetros
        context = {"course": course,
                   "name": username, 
                   "tried": tried, 
                   "user": request.session['user'], 
                   "role": request.session['role']}

        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_total_tried.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin visualización total intentos *****



# ***** Gráfica promedio intentos actividad *****
def average_tried_activity(request):    
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        context = {"course": course,
                   "user":   request.session['user'], 
                   "role":   request.session['role']}
    
        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_average_tried_activity.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin promedio intentos actividad *****



# ***** Visualización total intentos *****
def display_average_tried_activity(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        course = request.POST['cmbCourse']

        # Se ejecuta el query 
        select = (""" SELECT username, (SUM(tried)/COUNT(taskid)) AS promedio
                      FROM inginious.user_tasks
                      WHERE course_id = %(course)s
                      GROUP BY username
                      ORDER BY promedio DESC """)
        cursor.execute(select,{'course': course})
        record = cursor.fetchall()
        
        # Se definen los vectores para los elementos del reporte
        username = []
        average_tried = []

        for row in record:
            username.append(row[0])
            average_tried.append(float(row[1]))
        
        # Se consulta el nombre del curso
        cursor.execute(""" SELECT DISTINCT course_id
                           FROM inginious.user_tasks 
                           WHERE course_id IN ('FDP-2022-1', 'FDP-2022-2','FDP-01-2023-1') """)
        course = cursor.fetchall()

        # Se renderiza el Contexto con los parámetros
        context = {"course":        course,
                   "name":          username,
                   "average_tried": average_tried, 
                   "user":          request.session['user'], 
                   "role":          request.session['role']}

        # *** Plantilla ***
        return render(request, 'courses_reports/rpt_average_tried_activity.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin visualización total intentos *****

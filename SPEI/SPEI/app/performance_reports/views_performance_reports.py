# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de tiempo
import datetime


# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql


# ***** Desempeño por actividad *****
def performance_activity(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

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

        # Se consultan las tareas
        cursor.execute(""" SELECT task_name 
                           FROM early_intervention.tasks 
                           WHERE task_name IN ('Laboratorio1','Laboratorio2')
                           AND state = 'A' """)
        task = cursor.fetchall()

        context = {"course":    course,
                   "semester":  semester,
                   "task":      task, 
                   "user":      request.session['user'], 
                   "role":      request.session['role']}
    
        # *** Plantilla ***
        return render(request, 'performance_reports/rpt_performance_activity.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Desempeño por actividad *****


# ***** Visualización desempeño por actividad  *****
def display_performance_activity(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        course = request.POST['cmbCourse']
        semester = request.POST['cmbSemester']
        task = request.POST['cmbTask']

        # Se consulta el nombre del estudiante
        select = (""" SELECT realname 
                      FROM inginious.users
                      WHERE username = %(user)s  """)
        cursor.execute(select, {'user': request.POST['user']})
        student = cursor.fetchone()

        # Se consulta el id_courses_semesters
        select = (""" SELECT CS.id
                      FROM early_intervention.courses_semesters AS CS
                      INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id
                      INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                      WHERE C.course_name = %s
                      AND S.semester = %s 
                      AND CS.state = 'A' """)
        parameter = (course , semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Homologación de la tarea
        if task == 'Laboratorio1':
            # Se consulta la calificación del laboratorio1 
            select = (""" SELECT DISTINCT lab1 
                          FROM early_intervention.classification_data
                          WHERE student = %s
                          AND id_courses_semesters = %s """)
            parameter = (student[0] , id_courses_semesters[0])
            cursor.execute(select, parameter)
            student_grade = cursor.fetchone()

            # Se consulta el promedio del laboratorio 1 para el curso
            select = (""" SELECT avg(lab1) 
                          FROM early_intervention.classification_data
                          WHERE id_courses_semesters = %(id_courses_semesters)s  """)
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            course_avg = cursor.fetchone()

        elif task == 'Laboratorio2':
            # Se ejecuta el query para consultar la calificación del laboratorio1 
            select = (""" SELECT DISTINCT lab2 
                          FROM early_intervention.classification_data
                          WHERE student = %s
                          AND id_courses_semesters = %s """)
            parameter = (student[0] , id_courses_semesters[0])
            cursor.execute(select, parameter)
            student_grade = cursor.fetchone()

            # Se consulta el promedio del laboratorio 2 para el curso
            select = (""" SELECT avg(lab2) 
                          FROM early_intervention.classification_data
                          WHERE id_courses_semesters = %(id_courses_semesters)s  """)
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            course_avg = cursor.fetchone()

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

        # Se consultan las tareas
        cursor.execute(""" SELECT task_name 
                           FROM early_intervention.tasks 
                           WHERE task_name IN ('Laboratorio1','Laboratorio2')
                           AND state = 'A' """)
        task = cursor.fetchall()

        # Se cargan las variables de sesión al contexto
        context = {"course":          course,
                   "semester":        semester,
                   "task":            task, 
                   "student_grade":   student_grade[0], 
                   "course_avg":      round(course_avg[0],1), 
                   "user":            request.session['user'], 
                   "role":            request.session['role']}

        # *** Plantilla ***
        return render(request, 'performance_reports/rpt_performance_activity.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin visualización desempeño por actividad  *****


# ***** Desempeño Ponderado *****
def weighted_performance(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

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

        context = {"course":    course,
                   "semester":  semester,
                   "user":      request.session['user'], 
                   "role":      request.session['role']}
    
        # *** Plantilla ***
        return render(request, 'performance_reports/rpt_weighted_performance.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Desempeño por actividad *****
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
        cursor.execute(""" SELECT id, course_name 
                           FROM early_intervention.courses
                           WHERE state = 'A' """)
        course = cursor.fetchall()

        # Se consultan los semestres
        cursor.execute(""" SELECT id, semester 
                           FROM early_intervention.semesters 
                           WHERE state = 'A' """)
        semester = cursor.fetchall()

        # Se consultan las tareas
        cursor.execute(""" SELECT DISTINCT task_name 
                           FROM early_intervention.tasks 
                           WHERE task_name IN ('Laboratorio1','Laboratorio2','Laboratorio3')
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
        user = request.POST['user']
        course = request.POST['cmbCourse']
        semester = request.POST['cmbSemester']
        task = request.POST['cmbTask']

        # Se consulta el nombre del estudiante
        select = (""" SELECT realname 
                      FROM inginious.users
                      WHERE username = %(user)s  """)
        cursor.execute(select, {'user': user})
        student = cursor.fetchone()

        # Se consulta el id_courses_semesters
        select = (""" SELECT CS.id
                      FROM early_intervention.courses_semesters AS CS
                      INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id
                      INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                      WHERE C.id = %s
                      AND S.id = %s 
                      AND CS.state = 'A' """)
        parameter = (course , semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        ### Homologación de la tarea ###
        # Si la tarea es laboratorio1
        if task == 'Laboratorio1':
            # Se consulta la calificación del laboratorio1 
            select = (""" SELECT lab1
                          FROM early_intervention.regression_data
                          WHERE student = %s
                          AND id_courses_semesters = %s """)
            parameter = (student[0] , id_courses_semesters[0])
            cursor.execute(select, parameter)
            student_grade = cursor.fetchone()

            # Se consulta el promedio del laboratorio 1 para el curso
            select = (""" SELECT avg(lab1) 
                          FROM early_intervention.regression_data
                          WHERE id_courses_semesters = %(id_courses_semesters)s  """)
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            course_avg = cursor.fetchone()

        # Si la tarea es laboratorio2
        elif task == 'Laboratorio2':
            # Se ejecuta el query para consultar la calificación del laboratorio2 
            select = (""" SELECT lab2
                          FROM early_intervention.regression_data
                          WHERE student = %s
                          AND id_courses_semesters = %s """)
            parameter = (student[0] , id_courses_semesters[0])
            cursor.execute(select, parameter)
            student_grade = cursor.fetchone()

            # Se consulta el promedio del laboratorio 2 para el curso
            select = (""" SELECT avg(lab2) 
                          FROM early_intervention.regression_data
                          WHERE id_courses_semesters = %(id_courses_semesters)s  """)
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            course_avg = cursor.fetchone()
        
        # Si la tarea es laboratorio3
        elif task == 'Laboratorio3':
            # Se ejecuta el query para consultar la calificación del laboratorio3
            select = (""" SELECT lab3
                          FROM early_intervention.regression_data
                          WHERE student = %s
                          AND id_courses_semesters = %s """)
            parameter = (student[0] , id_courses_semesters[0])
            cursor.execute(select, parameter)
            student_grade = cursor.fetchone()

            # Se consulta el promedio del laboratorio 3 para el curso
            select = (""" SELECT avg(lab3) 
                          FROM early_intervention.regression_data
                          WHERE id_courses_semesters = %(id_courses_semesters)s  """)
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            course_avg = cursor.fetchone()

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

        # Se consultan las tareas
        cursor.execute(""" SELECT DISTINCT task_name 
                           FROM early_intervention.tasks 
                           WHERE task_name IN ('Laboratorio1','Laboratorio2','Laboratorio3')
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
        cursor.execute(""" SELECT id, course_name 
                           FROM early_intervention.courses
                           WHERE state = 'A' """)
        course = cursor.fetchall()

        # Se consultan los semestres
        cursor.execute(""" SELECT id, semester 
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

# ***** Fin Desempeño Ponderado *****



# ***** Visualización Desempeño Ponderado  *****
def display_weighted_performance(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        user = request.POST['user']
        course = request.POST['cmbCourse']
        semester = request.POST['cmbSemester']

        # Se consulta el nombre del estudiante
        select = (""" SELECT realname 
                      FROM inginious.users
                      WHERE username = %(user)s  """)
        cursor.execute(select, {'user': user})
        student = cursor.fetchone()

        # Se consulta el id_courses_semesters
        select = (""" SELECT CS.id
                      FROM early_intervention.courses_semesters AS CS
                      INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id
                      INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                      WHERE C.id = %s
                      AND S.id = %s 
                      AND CS.state = 'A' """)
        parameter = (course , semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Se consulta la calificación del estudiante para: laboratorio1, laboratorio2 y laboratorio3
        select = (""" SELECT lab1, lab2, lab3
                      FROM early_intervention.regression_data
                      WHERE student = %s
                      AND id_courses_semesters = %s """)
        parameter = (student[0] , id_courses_semesters[0])
        cursor.execute(select, parameter)
        student_grade = cursor.fetchone()

        # Se consulta el promedio del curso para: laboratorio1, laboratorio2 y laboratorio3
        select = (""" SELECT avg(lab1), avg(lab2), avg(lab3)
                      FROM early_intervention.regression_data
                      WHERE id_courses_semesters = %(id_courses_semesters)s  """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
        course_avg = cursor.fetchone()

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


        # Se cargan las variables de sesión al contexto
        context = {"course":          course,
                   "semester":        semester,
                   "student_grade":   student_grade, 
                   "course_avg":      course_avg, 
                   "user":            request.session['user'], 
                   "role":            request.session['role']}

        # *** Plantilla ***
        return render(request, 'performance_reports/rpt_weighted_performance.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Visualización Desempeño Ponderado  *****




# ***** Desempeño por Indicador de Logro *****
def achievement_indicator(request):
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

        context = {"course":    course,
                   "semester":  semester,
                   "user":      request.session['user'], 
                   "role":      request.session['role']}
    
        # *** Plantilla ***
        return render(request, 'performance_reports/rpt_achievement_indicator.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Desempeño por Indicador de Logro *****



# ***** Visualización Desempeño por Indicador de Logro  *****
def display_achievement_indicator(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        user = request.POST['user']
        course = request.POST['cmbCourse']
        semester = request.POST['cmbSemester']

        # Se consulta el nombre del estudiante
        select = (""" SELECT realname 
                      FROM inginious.users
                      WHERE username = %(user)s  """)
        cursor.execute(select, {'user': user})
        student = cursor.fetchone()

        # Se consulta el id_courses_semesters
        select = (""" SELECT CS.id
                      FROM early_intervention.courses_semesters AS CS
                      INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id
                      INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                      WHERE C.id = %s
                      AND S.id = %s 
                      AND CS.state = 'A' """)
        parameter = (course , semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Se consultan los registros en la Base de Datos
        select = (""" SELECT T.task_name, IA.code, IA.name, EA.points, SA.grade_indicator
                      FROM early_intervention.student_assessments AS SA
                      INNER JOIN early_intervention.evaluation_activity AS EA ON SA.id_evaluation_activity = EA.id 
                      INNER JOIN early_intervention.tasks AS T ON EA.id_tasks = T.id
                      INNER JOIN early_intervention.indicator_achievement AS IA ON EA.id_indicator_achievement = IA.id
                      WHERE SA.student_name = %s
                      AND EA.id_courses_semesters = %s
                      ORDER BY T.task_name, IA.code ASC """)
        parameter = (student[0], id_courses_semesters[0])
        cursor.execute(select, parameter)
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


        # Se cargan las variables de sesión al contexto
        context = {"course":    course,
                   "semester":  semester,
                   "record":    record,
                   "user":      request.session['user'], 
                   "role":      request.session['role']}

        # *** Plantilla ***
        return render(request, 'performance_reports/rpt_achievement_indicator.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Visualización Desempeño por Indicador de Logro  *****

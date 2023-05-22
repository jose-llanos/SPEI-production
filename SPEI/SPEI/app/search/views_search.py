# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de tiempo
import datetime

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql


# ***** Consultar Calificaciones Estudiante *****
def student_grade(request):
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
        return render(request, 'search/student_grade.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    
# ***** Fin Consultar Calificaciones Estudiante *****




# ***** Mostrar Calificaciones Estudinte *****
def show_student_grade(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']

        # Se consulta el id de courses_semesters
        select = (""" SELECT id 
                      FROM early_intervention.courses_semesters 
                      WHERE id_course = %s
                      AND id_semester = %s
                      AND state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Se buscan los registros en la Base de Datos
        select = (""" SELECT DISTINCT C.course_acronym, CD.student, CD.lab1, CD.lab2
                      FROM early_intervention.classification_data AS CD 
                      INNER JOIN early_intervention.courses_semesters AS CS ON CD.id_courses_semesters = CS.id
                      INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id
                      WHERE CD.id_courses_semesters = %(id_courses_semesters)s
                      ORDER BY CD.student ASC """)
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
        context = {"course":    course,
                   "semester":  semester,
                   "record":    record, 
                   "user":      request.session['user'], 
                   "role":      request.session['role']}

        # *** Plantilla ***
        return render(request, 'search/student_grade.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    
# ***** Fin Mostrar Calificaciones Estudinte  *****
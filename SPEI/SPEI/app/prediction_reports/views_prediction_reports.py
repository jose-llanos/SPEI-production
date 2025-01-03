# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de tiempo
import datetime

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql

# ***** Reporte de Columnas *****
def rpt_columns(request):    
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
        return render(request, 'prediction_reports/rpt_columns.html', context= context)
        
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión

# ***** Fin Reporte columnas *****



# ***** Visualización Columnas  *****
def column_display(request):
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

        # Se genera la busqueda en la BD
        select = (""" SELECT * 
                      FROM early_intervention.regression_data 
                      WHERE id_courses_semesters = %(id_courses_semesters)s
                      ORDER BY final_prediction ASC """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
        record = cursor.fetchall()

        # Defino los vectores para los elementos del reporte
        name = []
        average_grade = []
        final_grade_prediction = []

        for row in record:
            name.append(row[2])
            average_grade.append(float(row[8]))
            final_grade_prediction.append(float(row[9]))

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
        context = {"course":                 course,
                   "semester":               semester,
                   "name":                   name, 
                   "average_grade":          average_grade, 
                   "final_grade_prediction": final_grade_prediction,
                   "user":                   request.session['user'], 
                   "role":                   request.session['role']}

        # *** Plantilla ***
        return render(request, 'prediction_reports/rpt_columns.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Visualización Columnas  *****




# ***** Reporte de Líneas *****
def rpt_lines(request):
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
        return render(request, 'prediction_reports/rpt_lines.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Reporte lineas *****



# ***** Visualización Lineas  *****
def lines_display(request):
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

         # Se genera la busqueda en la BD
        select = (""" SELECT * 
                      FROM early_intervention.regression_data 
                      WHERE id_courses_semesters = %(id_courses_semesters)s
                      ORDER BY final_prediction ASC """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
        record = cursor.fetchall()

        # Defino los vectores para los elementos del reporte
        name = []
        average_grade = []
        final_grade_prediction = []

        for row in record:
            name.append(row[2])
            average_grade.append(float(row[8]))
            final_grade_prediction.append(float(row[9]))
        
        # Se consulta el nombre del curso
        cursor.execute(""" SELECT id,course_name 
                           FROM early_intervention.courses
                           WHERE state = 'A' """)
        course = cursor.fetchall()

        # Se consultan los semestres
        cursor.execute(""" SELECT id,semester 
                           FROM early_intervention.semesters 
                           WHERE state = 'A' """)
        semester = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros
        context = {"course":                 course,
                   "semester":               semester,
                   "name":                   name, 
                   "average_grade":          average_grade, 
                   "final_grade_prediction": final_grade_prediction,
                   "user":                   request.session['user'], 
                   "role":                   request.session['role']}

        # *** Plantilla ***
        return render(request, 'prediction_reports/rpt_lines.html', context= context)
    
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Visualización Lineas  *****
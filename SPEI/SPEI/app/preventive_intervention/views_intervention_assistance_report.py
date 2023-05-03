# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de fecha
from datetime import date, datetime

# Se importa la librería para envío de correos
from django.core.mail import EmailMessage

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql



# ***** Reporte Asistencia de Intervención *****
def intervention_assistance_report(request):
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

        context = {"course":   course,
                   "semester": semester, 
                   "user":     request.session['user'], 
                   "role":     request.session['role']}
        
        # *** Plantilla ***
        return render(request, 'preventive_intervention/intervention_assistance_report.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Reporte Asistencia de Intervención *****




# ***** Mostrar Reporte Asistencia de Intervención *****
def show_intervention_assistance_report(request):
    
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        student_record = []

        # Se consulta el id del semestre
        select = (""" SELECT id 
                      FROM early_intervention.semesters 
                      WHERE semester = %(semester)s 
                      AND state = 'A' """)
        cursor.execute(select, {'semester': cmb_semester})
        id_semester = cursor.fetchone()

        # Se consulta la cantidad de tutorías programadas  
        select = (""" SELECT count(*) AS contador
                      FROM early_intervention.intervention_assistance
                      WHERE id_semesters = %(semester)s """)
        cursor.execute(select, {'semester': id_semester})
        number_tutoring = cursor.fetchone()

        # Se consulta la cantidad de asistencias por estudiante
        select = (""" SELECT IAD.student, count(IAD.attended)
                      FROM early_intervention.intervention_assistance_detail AS IAD 
                      INNER JOIN early_intervention.intervention_assistance AS IA ON IAD.id_intervention_assistance = IA.id
                      WHERE IA.id_semesters = %(semester)s
                      AND IAD.attended = 1
                      GROUP BY IAD.student
                      ORDER BY IAD.student ASC """)
        cursor.execute(select, {'semester': id_semester})
        record = cursor.fetchall()

        # Se recorren todos los registros de los estudintes
        for row in record:
            student = row[0]

            # Se obtiene el número de asistencias
            number_assistance = int(row[1])
   
            # Se calcula el porcentaje de asistencias de intervención
            percentage_assistance = (number_assistance * 100) / number_tutoring[0]
            
            # Se consulta la calificación (lab1 y lab2) y predicción del estudiante
            select = (""" SELECT DISTINCT student, lab1, lab2, prediction
                          FROM early_intervention.classification_data
                          WHERE id_courses_semesters = %s
                          AND student = %s
                          ORDER BY student ASC """)
            parameter = (id_semester, student)
            cursor.execute(select, parameter)
            grade_record = cursor.fetchall()

            for row_grade in grade_record:
                lab1 = row_grade[1]
                lab2 = row_grade[2]
                average_grade = (lab1 + lab2) / 2
                prediction = row_grade[3]

            # Se cargan el registro al vector
            student_record.append([student, 
                                    lab1, 
                                    lab2, 
                                    average_grade, 
                                    prediction,
                                    number_tutoring[0], 
                                    number_assistance, 
                                    round(percentage_assistance,2)])

        context = {"course":   cmb_course,
                   "semester": cmb_semester,
                   "record":   student_record,
                   "user":  request.session['user'], 
                   "role":      request.session['role']}

        # *** Plantilla ***
        return render(request, 'preventive_intervention/intervention_assistance_report.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Reporte Asistencia de Intervención *****
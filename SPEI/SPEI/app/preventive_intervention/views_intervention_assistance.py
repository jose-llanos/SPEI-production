# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de fecha
from datetime import date, datetime

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql


# ***** Asistencia Intervención *****
def intervention_assistance(request):
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
        return render(request, 'preventive_intervention/intervention_assistance.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Asistencia Intervención *****


# ***** Control Asistencia Intervención *****
def control_intervention_assistance(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        btn_option = request.POST['btnOption']
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']

        # Se consulta el id del semestre
        select = (""" SELECT id 
                        FROM early_intervention.semesters
                        WHERE semester = %(semester)s 
                        AND state = 'A' """)
        cursor.execute(select, {'semester': cmb_semester})
        id_semester = cursor.fetchone()

        ### Nuevo ###
        # Si el botón seleccionado es nuevo
        if btn_option == "new":
            # Se consultan las fechas de tutoria para el curso
            select = (""" SELECT tutoring_date
                          FROM early_intervention.group_tutoring
                          WHERE id_semesters = %(semester)s """)
            cursor.execute(select, {'semester': id_semester[0]})
            record = cursor.fetchall()

            # Se formatea la fecha
            tutoring_date = []

            for row in record:
                row = str(row)
                row = row.replace("(datetime.date(","")
                row = row.replace("),)","")
                row = row.replace(", ","-")
                tutoring_date.append(row)

            # Se consultan los estudiantes del curso
            select = (""" SELECT DISTINCT id_courses_semesters, student 
                          FROM early_intervention.classification_data
                          WHERE id_courses_semesters = %(semester)s 
                          ORDER BY student ASC""")
            cursor.execute(select, {'semester': id_semester[0]})
            record = cursor.fetchall()

            context = {"course":        cmb_course, 
                       "semester":      cmb_semester,
                       "tutoring_date": tutoring_date, 
                       "record":        record, 
                       "usuario":       request.session['usuario'], 
                       "rol":           request.session['rol']}
        
            # *** Plantilla ***
            return render(request, 'preventive_intervention/new_intervention_assistance.html', context= context)

        ### Cargar ###
        # Si el botón seleccionado es cargar
        elif btn_option == "load":
            # Se cargan las asistencias de intervención
            context = view_intervention_assistance(request, cmb_course, cmb_semester, id_semester[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_assistance.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Control Asistencia Intervención *****

# ***** Modificar/Guardar Asistencia Intervención *****
def save_intervention_assistance(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        id = request.POST['txtId']
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        cmb_tutoring_date = request.POST['cmbTutoringDate']

        # Se consulta el id del semestre
        select = (""" SELECT id 
                      FROM early_intervention.semesters
                      WHERE semester = %(semester)s 
                      AND state = 'A' """)
        cursor.execute(select, {'semester': cmb_semester})
        id_semester = cursor.fetchone()
        
        ### Modificar ###
        # Si el registro existe se actualiza solo el detalle
        if id != "":
            # Se actualizan todos los registros del detalle (attended = 0) con base al id de la Asistencia de intervención
            update = """ UPDATE early_intervention.intervention_assistance_detail 
                         SET attended = '0'
                         WHERE id_intervention_assistance = %(id)s """
            cursor.execute(update, {'id': id})

            # Se recuperan los checkbox seleccionados (estudiantes que asistieron a la intervención)
            for item in request.POST.getlist('chkEstudiante'):
                # Se consulta el id del estudiante para realizar la actualización
                select = (""" SELECT IAD.id
                              FROM early_intervention.intervention_assistance_detail AS IAD
                              INNER JOIN early_intervention.intervention_assistance AS IA ON IAD.id_intervention_assistance = IA.id
                              WHERE IA.id_semesters = %s
                              AND IA.intervention_date = %s
                              AND IAD.student = %s """)
                parameter = (id_semester[0], cmb_tutoring_date, item)
                cursor.execute(select, parameter)
                id_student = cursor.fetchall()

                # Se actualiza el valor de attended a 1
                update = (""" UPDATE early_intervention.intervention_assistance_detail 
                              SET attended = 1
                              WHERE id = %s
                              AND student = %s """)
                parameter = (id_student[0], item)
                cursor.execute(update, parameter)

            # Se cargan las asistencias de intervención
            context = view_intervention_assistance(request, cmb_course, cmb_semester, id_semester[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_assistance.html', context= context)

        ### Guardar ###
        # Si no existe el registro se inserta en la cabecera y en el detalle
        elif id == "":
            # Se inserta la cabecera de la Asistencia de Intervención
            insert = (""" INSERT INTO early_intervention.intervention_assistance 
                          (id_semesters, intervention_date, state)
                          VALUES(%s, %s, %s) """)
            parameter = (id_semester[0], 
                         cmb_tutoring_date, 
                         'A')
            cursor.execute(insert, parameter)

            # Se consulta el último registro insertado en Asistencia de Intervención
            cursor.execute(""" SELECT MAX(id) 
                               FROM early_intervention.intervention_assistance """)
            id_intervention_assistance = cursor.fetchone()


            # Se consultan los estudiantes del curso para insertar el detalle de la Asistencia de Intervención
            select = (""" SELECT DISTINCT student 
                          FROM early_intervention.classification_data
                          WHERE id_courses_semesters = %(semesters)s 
                          ORDER BY student ASC""")
            cursor.execute(select, {'semesters': id_semester[0]})
            record = cursor.fetchall()

            # Se recorre el ciclo de los estudiantes del curso
            for student in record:
                # Se insertan todos los registros del detalle de Asistencia de Intervención con attended igual a 0
                insert = (""" INSERT INTO early_intervention.intervention_assistance_detail 
                              (id_intervention_assistance, student, attended)
                              VALUES(%s, %s, %s) """)
                parameter = (id_intervention_assistance[0], 
                             student, 
                             '0')
                cursor.execute(insert, parameter)

            # Se recuperan los checkbox seleccionados (estudiantes que asistieron a la intervención)
            for item in request.POST.getlist('chkEstudiante'):
                # Se actualiza el valor de attended a 1
                update = (""" UPDATE early_intervention.intervention_assistance_detail 
                              SET attended = 1
                              WHERE id_intervention_assistance = %s
                              AND  student = %s """)
                parameter = (id_intervention_assistance[0], 
                             item)
                cursor.execute(update, parameter)
            
            # Se cargan las asistencias de intervención
            context = view_intervention_assistance(request, cmb_course, cmb_semester, id_semester[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_assistance.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Modificar/Guardar Asistencia Intervención  *****


# ***** Operación Asistencia Intervención *****
def operation_intervention_assistance(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        operation = request.POST['idOperation']
        operation = operation.replace(" ","")
        operation = operation.split("-")

        # Se consulta el id del semestre
        select = (""" SELECT id 
                      FROM early_intervention.semesters
                      WHERE semester = %(semester)s 
                      AND state = 'A' """)
        cursor.execute(select, {'semester': cmb_semester})
        id_semester = cursor.fetchone()
        
        ### Modificar ###
        # Si el botón opción es modificar
        if operation[0] == "update":
            # Se trae el id a modificar
            id = operation[1]

            # Se consulta la cabecera de Asistencia de Intervencion
            select = (""" SELECT intervention_date
                          FROM early_intervention.intervention_assistance 
                          WHERE id = %(id)s
                          AND state = 'A'  """)
            cursor.execute(select, {'id': id})
            record = cursor.fetchall()

            # Se formatea la fecha
            tutoring_date = []

            for row in record:
                row = str(row)
                row = row.replace("(datetime.date(","")
                row = row.replace("),)","")
                row = row.replace(", ","-")
                tutoring_date.append(row)

            # Se consulta el detalle de Asistencia de Intervención
            select = (""" SELECT IA.id_semesters, IAD.student, IAD.attended
                          FROM early_intervention.intervention_assistance_detail AS IAD
                          INNER JOIN early_intervention.intervention_assistance AS IA ON IAD.id_intervention_assistance = IA.id
                          WHERE IA.id_semesters = %s
                          AND IAD.id_intervention_assistance = %s 
                          ORDER BY IAD.student ASC""")
            parameter = (id_semester[0], id )
            cursor.execute(select, parameter)
            record = cursor.fetchall()

            context = {"id":                     id,
                       "course":                 cmb_course, 
                       "semester":               cmb_semester, 
                       "tutoring_date":          tutoring_date,
                       "record":                 record, 
                       "user":                   request.session['user'], 
                       "role":                   request.session['role']}
        
            # *** Plantilla ***
            return render(request, 'preventive_intervention/new_intervention_assistance.html', context= context)

        ### Eliminar ###
        # Si el botón opción es eliminar
        elif operation[0] == "delete":
            id = operation[1]

            # Se actualiza el registro de la tabla intervention_assistance
            update = (""" UPDATE early_intervention.intervention_assistance 
                          SET state = 'I'
                          WHERE id = %(id)s """)
            cursor.execute(update, {'id': id})

            # Se cargan las asistencias de intervención
            context = view_intervention_assistance(request, cmb_course, cmb_semester, id_semester[0])
        
            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_assistance.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Operación Asistencia Intervención *****


# ***** Ver Asitencia de Intervención *****
def view_intervention_assistance(request, cmb_course, cmb_semester, id_semester):
    # Se genera la conexión con la base de datos
    cursor = connection_postgresql()

    # Se consultan los registros de la tabla intervention_message
    select = (""" SELECT id, id_semesters, intervention_date
                  FROM early_intervention.intervention_assistance 
                  WHERE id_semesters = %(semester)s
                  AND state = 'A' """)
    cursor.execute(select, {'semester': id_semester})
    record = cursor.fetchall()

    context = {"record":   record, 
               "course":   cmb_course, 
               "semester": cmb_semester,
               "user":     request.session['user'], 
               "role":     request.session['role']}

    return context
# ***** Fin ver Asistencia de Intervención *****
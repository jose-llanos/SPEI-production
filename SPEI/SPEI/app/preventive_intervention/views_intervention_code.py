# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de fecha
from datetime import date, datetime

# Se importa la librería para envío de correos
from django.core.mail import EmailMessage

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql


# ***** Intervención Código *****
def intervention_code(request):
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
        return render(request, 'preventive_intervention/intervention_code.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Intervención Código *****



# ***** Control Intervención Código *****
def control_intervention_code(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        btn_option = request.POST['btnOption']
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']

        ### Nuevo ###
        # Si el botón seleccionado es nuevo
        if btn_option == "new":
            # Se consultan las tareas
            cursor.execute(""" SELECT task_name 
                               FROM early_intervention.tasks 
                               WHERE state = 'A' """)
            task = cursor.fetchall()

            context = {"course":   cmb_course,
                       "semester": cmb_semester,
                       "task":     task, 
                       "user":     request.session['user'], 
                       "role":     request.session['role']}

            # *** Plantilla ***
            return render(request, 'preventive_intervention/new_intervention_code.html', context= context)

        ### Mostrar ###
        # Si el botón seleccionado es mostrar
        elif btn_option == "load":
            # Se consulta el id del curso
            select = (""" SELECT id
                          FROM early_intervention.courses
                          WHERE course_name = %(course)s 
                          AND state = 'A' """)
            cursor.execute(select, {'course': cmb_course})
            id_course = cursor.fetchone()

            # Se cargan las intervenciones con codigo
            context = view_intervention_code(request, cmb_course, cmb_semester, id_course[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_code.html', context= context)
            
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Control Intervención Código *****



# ***** Cargar codigo *****
def upload_code(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        id = request.POST['txtId']
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        message = request.POST['txtMessage']
        selected_task = request.POST['cmbTask']

        # Se cargan las tareas en un vector
        cursor.execute(""" SELECT task_name 
                           FROM early_intervention.tasks 
                           WHERE state = 'A' """)
        task = cursor.fetchall()

        # Se ejecuta el query para mostrar el código fuente (plantilla)
        select = (""" SELECT RC.reference_code
                      FROM early_intervention.tasks AS T
                      INNER JOIN early_intervention.reference_code AS RC 
                      ON T.id = RC.id_task
                      WHERE T.task_name = %(selected_task)s """)
        cursor.execute(select, {'selected_task': selected_task})
        record = cursor.fetchall()

        # Se formatea el código fuente
        code = format_code(record)

        context = {"id":            id,
                   "course":        cmb_course, 
                   "semester":      cmb_semester,
                   "message":       message, 
                   "selected_task": selected_task,
                   "task":          task,
                   "code":          code,
                   "user":          request.session['user'], 
                   "role":          request.session['role']}
        # *** Plantilla ***
        return render(request, 'preventive_intervention/new_intervention_code.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Cargar Codigo *****


# ***** Modificar/Guardar Intervención Código *****
def save_intervention_code(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        id = request.POST['txtId']
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        txt_message = request.POST['txtMessage']
        cmb_task = request.POST['cmbTask']

        # Se consulta el id del curso
        select = (""" SELECT id
                      FROM early_intervention.courses
                      WHERE course_name = %(course)s 
                      AND state = 'A' """)
        cursor.execute(select, {'course': cmb_course})
        id_course = cursor.fetchone()

        # Se consulta el id del task
        select = (""" SELECT id
                      FROM early_intervention.tasks
                      WHERE task_name = %(task)s 
                      AND state = 'A' """)
        cursor.execute(select, {'task': cmb_task})
        id_task = cursor.fetchone()

        # Se consulta el id de reference_code
        select = (""" SELECT RC.id
                      FROM early_intervention.tasks AS T
                      INNER JOIN early_intervention.reference_code AS RC
                      ON T.id = RC.id_task
                      WHERE T.task_name = %(task)s 
                      AND T.state = 'A' """)
        cursor.execute(select, {'task': cmb_task})
        id_reference_code = cursor.fetchone()

        ### Modificar ###
        # Si el registro existe se actualiza solo el detalle
        if id != "":
            # Se modifica el registro en la tabla: intervention_message
            update = """ UPDATE early_intervention.intervention_code 
                         SET id_tasks = %s,
                         id_reference_code = %s,
                         message = %s
                         WHERE id = %s """
            parameter = (id_task[0],
                         id_reference_code[0], 
                         txt_message, 
                         id)
            cursor.execute(update, parameter)

            # Se cargan las intervenciones con código
            context = view_intervention_code(request, cmb_course, cmb_semester, id_course[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_code.html', context= context)
            

        ### Guardar ###
        # Si no existe el registro se inserta el registro en la tabla
        elif id == "":
            # Se definen los vectores de email prueba
            student_email = []
            today = date.today()

            # Se consulta el valor de la predicción
            select = (""" SELECT DISTINCT U.email
                          FROM early_intervention.classification_data AS CD, inginious.users AS U
                          WHERE CD.student = U.realname
                          AND CD.id_courses_semesters = 3 """)
            cursor.execute(select, {'semester': cmb_semester[0]})
            record = cursor.fetchall()
            
            # Se envía el email a cada estudiante
            for email in record:
                email = str(email)
                email = email.replace("('","")
                email = email.replace("',)","")
                student_email.append(email)

            # Se envía copia del mensaje
            student_email.append('jose.llanos@correounivalle.edu.co')

            subject = 'Intervención Preventiva SPEI: Código Fuente Referencia'
            message = txt_message
            email_from = 'ing.jose.llanos@gmail.com'
            email_to = student_email
            
            mail = EmailMessage(
                subject,
                message,
                email_from,
                email_to, 
            )
            #mail.attach_file('SPEI/data/lab1-p1.cpp')
            #mail.attach_file('SPEI/data/lab1-p2.cpp')
            #mail.attach_file('SPEI/data/lab2-p1.cpp')
            #mail.attach_file('SPEI/data/lab2-p2.cpp')
            mail.attach_file('SPEI/data/lab3-p1.cpp')
            mail.attach_file('SPEI/data/lab3-p2.cpp')
            mail.send()

            # Se guarda el registro en la tabla: intervention_suggestion
            insert = (""" INSERT INTO early_intervention.intervention_code 
                          (id_courses, id_tasks, id_reference_code, message, students, date, state)
                          VALUES(%s, %s, %s, %s, %s, %s, %s) """)
            parameter = (id_course[0], 
                         id_task[0],
                         id_reference_code[0], 
                         message, 
                         student_email, 
                         str(today), 
                         'A')
            cursor.execute(insert, parameter)

            # Se cargan las intervenciones con codigo
            context = view_intervention_code(request, cmb_course, cmb_semester, id_course[0])
            
            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_code.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Modificar/Guardar Intervención Código  *****



# ***** Operación Intervención Código *****
def operation_intervention_code(request):
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

        ### Modificar ###
        # Si el botón opción es modificar
        if operation[0] == "update":
            # Se trae el id a modificar
            id = operation[1]

            # Se consulta la Intervención con código
            select = (""" SELECT T.task_name, RC.reference_code, IC.message
                          FROM early_intervention.intervention_code AS IC
                          INNER JOIN early_intervention.tasks AS T ON IC.id_tasks = T.id
                          INNER JOIN early_intervention.reference_code AS RC ON IC.id_reference_code = RC.id
                          WHERE IC.id = %(id)s
                          AND IC.state = 'A'  """)
            cursor.execute(select, {'id': id})
            record = cursor.fetchall()

            for row in record:
                selected_task = str(row[0])
                code = row[1]
                message = row[2]
                
            
            # Se consultan las tareas
            cursor.execute(""" SELECT task_name 
                               FROM early_intervention.tasks 
                               WHERE state = 'A' """)
            task = cursor.fetchall()
             
            # Se formatea el código fuente
            code = format_code(code)

            context = {"id":            id,
                       "course":        cmb_course, 
                       "semester":      cmb_semester, 
                       "message":       message,
                       "selected_task": selected_task,
                       "task":          task,
                       "code":          code,
                       "user":          request.session['user'], 
                       "role":          request.session['role']}
            
            # *** Plantilla ***
            return render(request, 'preventive_intervention/new_intervention_code.html', context= context)

        ### Eliminar ###
        # Si el botón opción es eliminar
        elif operation[0] == "delete":
            id = operation[1]

            # Se consulta el id del curso
            select = (""" SELECT id
                          FROM early_intervention.courses
                          WHERE course_name = %(course)s 
                          AND state = 'A' """)
            cursor.execute(select, {'course': cmb_course})
            id_course = cursor.fetchone()

            # Se actualiza el registro de la tabla intervention_code
            update = (""" UPDATE early_intervention.intervention_code
                          SET state = 'I'
                          WHERE id = %(id)s """)
            cursor.execute(update, {'id': id})

            # Se cargan las intervenciones con codigo
            context = view_intervention_code(request, cmb_course, cmb_semester, id_course[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_code.html', context= context)
            
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Operación Intervención Código *****


# ***** Ver Intervención Código *****
def view_intervention_code(request, cmb_course, cmb_semester, id_course):
    # Se genera la conexión con la base de datos
    cursor = connection_postgresql()

    # Se consultan los registros de la tabla intervention_code, courses y reference_code
    select = (""" SELECT IC.id, C.course_name, T.task_name, IC.id_reference_code, IC.message, IC.date
                  FROM early_intervention.intervention_code AS IC
                  INNER JOIN early_intervention.courses AS C ON IC.id_courses = C.id
                  INNER JOIN early_intervention.tasks AS T ON IC.id_tasks = T.id
                  INNER JOIN early_intervention.reference_code AS RC ON IC.id_reference_code = RC.id
                  WHERE IC.id_courses = %(id_course)s
                  AND IC.state = 'A' """)
    cursor.execute(select, {'id_course': id_course})
    record = cursor.fetchall()

    context = {"record":   record, 
               "course":   cmb_course, 
               "semester": cmb_semester,
               "user":     request.session['user'], 
               "role":     request.session['role']}

    return context
# ***** Fin ver Intervención Código *****



# ***** Formatear código fuente *****
def format_code(record):
    code = "\n"

    record = str(record)
    separator = "#"
    record = record.split(separator)

    for row in record:
        row = str(row)
        row = row.replace("[('", "")
        row = row.replace("',)]", "")
        code += row
        code += "\n"
    
    return code
# ***** Fin formatear código fuente *****
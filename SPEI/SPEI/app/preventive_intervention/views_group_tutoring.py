# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de fecha
from datetime import date, datetime

# Se importa la librería para envío de correos
from django.core.mail import EmailMessage

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql


# ***** Tutoría Grupal *****
def group_tutoring(request):
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
        return render(request, 'preventive_intervention/group_tutoring.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Tutoría Grupal *****



# ***** Control Tutoría Grupal *****
def control_group_tutoring(request):
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
            # Se consultan los temas de intervención
            cursor.execute(""" SELECT topic 
                               FROM early_intervention.intervention_topics 
                               WHERE state = 'A' """)
            topic_intervention = cursor.fetchall()

            context = {"course":             cmb_course, 
                       "semester":           cmb_semester,
                       "topic_intervention": topic_intervention}

            # *** Plantilla ***
            return render(request, 'preventive_intervention/new_group_tutoring.html', context= context)

        ### Mostrar ###
        # Si el botón seleccionado es mostrar
        elif btn_option == "load":
            # Se consulta el id del semestre
            select = (""" SELECT id 
                          FROM early_intervention.semesters 
                          WHERE semester = %(semester)s 
                          AND state = 'A' """)
            cursor.execute(select, {'semester': cmb_semester})
            id_semester = cursor.fetchone()

            # Se cargan las tutorías grupales
            context = view_group_tutoring(request, cmb_course, cmb_semester, id_semester[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_group_tutoring.html', context= context)
            
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Control Tutoría Grupal *****



# ***** Modificar/Guardar Tutoría Grupal *****
def save_group_tutoring(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        id = request.POST['txtId']
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        cmb_topic_intervention = request.POST['cmbTopicIntervention']
        txt_tutoring_date = request.POST['txtTutoringDate']
        txt_tutoring_hour = request.POST['txtTutoringHour']
        txt_tutoring_site = request.POST['txtTutoringSite']
        txt_message = request.POST['txtMessage']

        # Se consulta el id del semestre
        select = (""" SELECT id 
                      FROM early_intervention.semesters 
                      WHERE semester = %(semester)s 
                      AND state = 'A' """)
        cursor.execute(select, {'semester': cmb_semester})
        id_semester = cursor.fetchone()

        # Se consulta el id de intervencion_topics
        select = (""" SELECT id 
                      FROM early_intervention.intervention_topics 
                      WHERE topic = %(topic)s 
                      AND state = 'A' """)
        cursor.execute(select, {'topic': cmb_topic_intervention})
        id_intervention_topic = cursor.fetchall()

        ### Modificar ###
        # Si el registro existe se actualiza solo el detalle
        if id != "":
            # Se modifica el registro en la tabla
            update = """ UPDATE early_intervention.group_tutoring
                         SET id_intervention_topic = %s,
                         tutoring_date = %s,
                         tutoring_hour = %s,
                         tutoring_site = %s,
                         message = %s
                         WHERE id = %s """
            parameter = (id_intervention_topic[0], 
                         txt_tutoring_date,
                         txt_tutoring_hour, 
                         txt_tutoring_site,
                         txt_message, 
                         id)
            cursor.execute(update, parameter)

            # Se cargan las intervenciones grupales
            context = view_group_tutoring(request, cmb_course, cmb_semester, id_semester[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_group_tutoring.html', context= context)
            

        ### Guardar ###
        # Si no existe el registro se inserta el registro en la tabla
        elif id == "":
            
            # Se definen los vectores para enviar el email de forma masiva
            student_email = []
            test_email = []
            today = date.today()

            # Se consulta el email de todos los estudiantes que pertenecen al curso
            select = (""" SELECT DISTINCT U.email
                          FROM early_intervention.classification_data AS CD, inginious.users AS U
                          WHERE CD.student = U.realname
                          AND CD.id_courses_semesters = %(semester)s """)
            cursor.execute(select, {'semester': id_semester[0]})

            record = cursor.fetchall()

            # Se carga el vector (email_estudiante) con los registros de la BD
            for email in record:
                email = str(email)
                email = email.replace("('","")
                email = email.replace("',)","")
                student_email.append(email)
            
            # Se envía el email a cada estudiante
            #email_estudiante.append('jose.llanos@correounivalle.edu.co' )
            test_email.append('chepe159@gmail.com')


            subject = "Tutoría Grupal: " + str(cmb_topic_intervention)
            message =  "Curso: "     + str(cmb_course)         + "\n"
            message += "Semestre: "  + str(cmb_semester)       + "\n"
            message += "Fecha: "     + str(txt_tutoring_date)  + "\n"
            message += "Hora: "      +  str(txt_tutoring_hour) + "\n"
            message += "Lugar: "     + str(txt_tutoring_site)  + "\n"
            message += "Mensaje: "   + str(txt_message)
            email_from = 'ing.jose.llanos@gmail.com'
            email_to = test_email
            #reply_to = 'ing.jose.llanos@gmail.com'
            
            mail = EmailMessage(
                subject,
                message,
                email_from,
                email_to, 
            )
            mail.send()

            # Se guarda el registro en la tabla: intervention_message
            insert = (""" INSERT INTO early_intervention.group_tutoring 
                          (id_semesters, id_intervention_topic,
                           tutoring_date, tutoring_hour,
                           tutoring_site, message, students, date, state)
                          VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'A') """)
            parameter = (id_semester[0],
                         id_intervention_topic[0], 
                         txt_tutoring_date,
                         txt_tutoring_hour,
                         txt_tutoring_site,
                         str(subject + "\n" + message), 
                         str(student_email), 
                         str(today))
            cursor.execute(insert, parameter)

            # Se cargan las tutorías grupales
            context = view_group_tutoring(request, cmb_course, cmb_semester, id_semester[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_group_tutoring.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Modificar/Guardar Tutoría Grupal  *****



# ***** Operación Tutoría Grupal *****
def operation_group_tutoring(request):
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
        id_semester = cursor.fetchall()

        # Se consultan los temas de intervención
        cursor.execute(""" SELECT topic 
                           FROM early_intervention.intervention_topics 
                           WHERE state = 'A' """)
        topic_intervention = cursor.fetchall()

        ### Modificar ###
        # Si el botón opción es modificar
        if operation[0] == "update":
            # Se trae el id a modificar
            id = operation[1]

            # Se consulta la Tutoría Grupal
            select = (""" SELECT IT.topic, GT.tutoring_date, GT.tutoring_hour, GT.tutoring_site, GT.message
                          FROM early_intervention.group_tutoring AS GT
                          INNER JOIN early_intervention.intervention_topics AS IT ON GT.id_intervention_topic = IT.id 
                          WHERE GT.id_semesters = %s
                          AND GT.id = %s
                          AND GT.state = 'A'  """)
            parameter = (id_semester[0], id)
            cursor.execute(select, parameter)
            record = cursor.fetchall()

            for row in record:
                topic = str(row[0])
                tutoring_date = str(row[1])
                tutoring_hour = str(row[2])
                tutoring_site = str(row[3])
                message       = str(row[4])

            context = {"id":                          id,
                       "course":                      cmb_course, 
                       "semester":                    cmb_semester, 
                       "selected_topic_intervention": topic,
                       "topic_intervention":          topic_intervention,
                       "tutoring_date":               tutoring_date,
                       "tutoring_hour":               tutoring_hour,
                       "tutoring_site":               tutoring_site,
                       "message":                     message,
                       "user":                        request.session['user'], 
                       "role":                        request.session['role']}
        
            # *** Plantilla ***
            return render(request, 'preventive_intervention/new_group_tutoring.html', context= context)

        ### Eliminar ###
        # Si el botón opción es eliminar
        elif operation[0] == "delete":
            
            id = operation[1]

            # Se actualiza el registro de la tabla 
            update = (""" UPDATE early_intervention.group_tutoring 
                          SET state = 'I'
                          WHERE id = %(id)s """)
            cursor.execute(update, {'id': id})

            # Se cargan las intervenciones con mensaje
            context = view_group_tutoring(request, cmb_course, cmb_semester, id_semester[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_group_tutoring.html', context= context)
            
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Operación Tutoría Grupal *****


# ***** Ver Tutorías Grupales *****
def view_group_tutoring(request, cmb_course, cmb_semester, id_semester):
    # Se genera la conexión con la base de datos
    cursor = connection_postgresql()

    # Se consultan los registros de la tabla intervention_message
    select = (""" SELECT GT.id, IT.topic, GT.tutoring_date, GT.tutoring_hour, GT.tutoring_site, GT.message
                  FROM early_intervention.group_tutoring AS GT
                  INNER JOIN early_intervention.intervention_topics AS IT ON GT.id_intervention_topic = IT.id
                  WHERE GT.id_semesters = %(semester)s
                  AND GT.state = 'A' """)
    cursor.execute(select, {'semester': id_semester})

    record = cursor.fetchall()

    context = {"record":   record, 
               "course":   cmb_course, 
               "semester": cmb_semester,
               "user":     request.session['user'], 
               "role":     request.session['role']}

    return context
# ***** Fin Ver Tutorías Grupales *****
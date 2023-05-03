# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de fecha
from datetime import date, datetime

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql

# Se importa la librería para envío de correos
from django.core.mail import EmailMessage


# ***** Intervención Sugerencia *****
def intervention_suggestion(request):
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
        return render(request, 'preventive_intervention/intervention_suggestion.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Intervención Sugerencia *****



# ***** Control Intervención Sugencia *****
def control_intervention_suggestion(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        btn_option = request.POST['btnOption']
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']

        # Se consulta el id de courses_semesters
        select = (""" SELECT CS.id 
                      FROM early_intervention.courses_semesters AS CS
                      INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id 
                      INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                      WHERE C.course_name = %s
                      AND S.semester = %s
                      AND CS.state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        ### Nuevo ###
        # Si el botón seleccionado es nuevo
        if btn_option == "new":

            # Se consulta los estudiantes a intervenir
            select = (""" SELECT DISTINCT CD.student
                          FROM early_intervention.classification_data AS CD, inginious.users AS U
                          WHERE CD.student = U.realname
                          AND CD.id_courses_semesters = %(id_courses_semesters)s
                          AND CD.prediction <> 2 
                          AND CD.prediction <> -1""")
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            student = cursor.fetchall()

            # Se consultan los indicadores de logro para el curso
            select = (""" SELECT id, code, name 
                          FROM early_intervention.indicator_achievement
                          WHERE id_courses_semesters = %(id_courses_semesters)s 
                          AND state = 'A' """)
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            il = cursor.fetchall()
            
            context = {"course":            cmb_course, 
                       "semester":          cmb_semester, 
                       "student_intervene": student,
                       "il":                il}

            # *** Plantilla ***
            return render(request, 'preventive_intervention/new_intervention_suggestion.html', context= context)

        ### Mostrar ###
        # Si el botón seleccionado es mostrar
        elif btn_option == "load":
            # Se cargan las intervenciones con sugerencia
            context = view_intervention_suggestion(request, cmb_course, cmb_semester, id_courses_semesters[0])

            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_suggestion.html', context= context)
            
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Control Intervención Sugerencia *****



# ***** Cargar Sugerencia *****
def upload_suggestion(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        txt_Id = request.POST['txtId']
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        txt_student_intervene = request.POST['txtStudentIntervene']
        selected_il = request.POST['cmbIl']

        # Se consulta el id de courses_semesters
        select = (""" SELECT CS.id 
                      FROM early_intervention.courses_semesters AS CS
                      INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id 
                      INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                      WHERE C.course_name = %s
                      AND S.semester = %s
                      AND CS.state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        # Se consulta el indicador seleccionado para el curso 
        select = (""" SELECT code, name 
                      FROM early_intervention.indicator_achievement
                      WHERE id = %(selected_il)s """)
        cursor.execute(select, {'selected_il': selected_il})
        il_selected = cursor.fetchone()

        il_selected = str(il_selected)
        il_selected = il_selected.replace("('", "")
        il_selected = il_selected.replace("', '", " - ")
        il_selected = il_selected.replace("')", "")

        # Se consultan los indicadores de logro para el curso
        select = (""" SELECT id, code, name 
                      FROM early_intervention.indicator_achievement
                      WHERE id_courses_semesters = %(id_courses_semesters)s 
                      AND state = 'A' """)
        cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
        il = cursor.fetchall()

        # Se consulta la sugerencia
        select = (""" SELECT suggestion 
                      FROM early_intervention.suggestions 
                      WHERE id_indicator_achievement = %(selected_il)s 
                      AND state = 'A' """)
        cursor.execute(select, {'selected_il': selected_il})
        record = cursor.fetchall()

        record = str(record)
        record = record.replace("[('", "")
        record = record.replace("',)]", "")

        context = {"id":                txt_Id,
                   "course":            cmb_course, 
                   "semester":          cmb_semester, 
                   "student_intervene": txt_student_intervene,
                   "selected_il":       il_selected,
                   "il":                il,
                   "suggestion":        record, 
                   "user":              request.session['user'], 
                   "role":              request.session['role']}
        # *** Plantilla ***
        return render(request, 'preventive_intervention/new_intervention_suggestion.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Cargar Sugerencia *****



# ***** Modificar/Guardar Intervención Sugerencia *****
def save_intervention_suggestion(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        id = request.POST['txtId']
        cmb_course = request.POST['cmbCourse']
        cmb_semester = request.POST['cmbSemester']
        cmb_il = request.POST['cmbIl']
        txt_suggestion = request.POST['txtSuggestion']
        today = date.today()

        # Se consulta el id de courses_semesters
        select = (""" SELECT CS.id 
                      FROM early_intervention.courses_semesters AS CS
                      INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id 
                      INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                      WHERE C.course_name = %s
                      AND S.semester = %s
                      AND CS.state = 'A' """)
        parameter = (cmb_course, cmb_semester)
        cursor.execute(select, parameter)
        id_courses_semesters = cursor.fetchone()

        ### Modificar ###
        # Si el registro existe se actualiza
        if id != "":
            # Se modifica el registro en la tabla: intervention_suggestion
            update = """ UPDATE early_intervention.intervention_suggestion
                         SET suggestion = %s
                         WHERE id = %s """
            parameter = (txt_suggestion, id)
            cursor.execute(update, parameter)

            # Se cargan las intervenciones con sugerencia
            context = view_intervention_suggestion(request, cmb_course, cmb_semester, id_courses_semesters[0])
            
            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_suggestion.html', context= context)
            

        ### Guardar ###
        # Si no existe el registro se inserta en la tabla
        elif id == "":

            # Se utilizan los valores que llegan del formulario
            il_name = cmb_il.split(" - ")
            il_name = il_name[1].replace("')", "")
            student_email = []
            test_email = []
            message = "--------------------------------------\n"
            message += "Indicador de logro evaluado:\n "
            message += "--------------------------------------\n" 
            message += cmb_il
            message += "\n"
            message += "--------------------------------------\n"
            message += "Sugerencia/Recomendación:\n"
            message += "--------------------------------------\n"
            message += txt_suggestion

            # Se consulta el id del indicador de logro
            select = (""" SELECT id 
                          FROM early_intervention.indicator_achievement
                          WHERE name LIKE %(il_name)s 
                          AND state = 'A' """)
            cursor.execute(select, {'il_name': il_name})
            id_il = cursor.fetchone()
            
            # Se consulta los estudiantes a intervenir
            select = (""" SELECT DISTINCT U.email
                          FROM early_intervention.classification_data AS CD, inginious.users AS U
                          WHERE CD.student = U.realname
                          AND CD.id_courses_semesters = %(id_courses_semesters)s
                          AND CD.prediction <> 2 
                          AND CD.prediction <> -1 """)
            cursor.execute(select, {'id_courses_semesters': str(id_courses_semesters[0])})
            record = cursor.fetchall()


            # Se envía el email a cada estudiante
            for email in record:
                email = str(email)
                email = email.replace("('","")
                email = email.replace("',)","")
                student_email.append(email)
            
            # Se envía copia del mensaje
            student_email.append('jose.llanos@correounivalle.edu.co')

            affair = 'Intervención Preventiva SPEI: Sugerencia/Recomendación'
            message = message
            email_from = 'ing.jose.llanos@gmail.com'
            email_to = student_email
            
            mail = EmailMessage(
                affair,
                message,
                email_from,
                email_to, 
            )
            
            mail.send()

            # Se guarda el registro en la tabla: intervention_suggestion
            insert = (""" INSERT INTO early_intervention.intervention_suggestion 
                          (id_courses_semesters, id_indicator_achievement, suggestion, students, date, state)
                          VALUES(%s, %s, %s, %s, %s, %s) """)
            parameter = (id_courses_semesters[0], 
                         id_il[0], 
                         message, 
                         str(student_email), 
                         str(today), 
                         'A')
            cursor.execute(insert, parameter)

            # Se cargan las intervenciones con sugerencia
            context = view_intervention_suggestion(request, cmb_course, cmb_semester, id_courses_semesters[0])
            
            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_suggestion.html', context= context)

    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Modificar/Guardar Intervención Sugerencia  *****



# ***** Operación Intervención Sugerencia *****
def operation_intervention_suggestion(request):
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
            # Se trae el id para modificar
            id = operation[1]

            # Se consulta el id de courses_semesters
            select = (""" SELECT CS.id 
                        FROM early_intervention.courses_semesters AS CS
                        INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id 
                        INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                        WHERE C.course_name = %s
                        AND S.semester = %s
                        AND CS.state = 'A' """)
            parameter = (cmb_course, cmb_semester)
            cursor.execute(select, parameter)
            id_courses_semesters = cursor.fetchone()

            # Se consultan los indicadores de logro para el curso
            select = (""" SELECT id, code, name 
                            FROM early_intervention.indicator_achievement
                            WHERE id_courses_semesters = %(id_courses_semesters)s 
                            AND state = 'A' """)
            cursor.execute(select, {'id_courses_semesters': id_courses_semesters[0]})
            il = cursor.fetchall()

            # Se consulta la Intervención con Sugerencia
            select = (""" SELECT IA.name, ISU.suggestion, ISU.students
                          FROM early_intervention.intervention_suggestion AS ISU
                          INNER JOIN early_intervention.courses_semesters AS CS ON ISU.id_courses_semesters = CS.id
                          INNER JOIN early_intervention.indicator_achievement AS IA ON ISU.id_indicator_achievement = IA.id
                          WHERE ISU.id = %(id)s
                          AND ISU.state = 'A'  """)
            cursor.execute(select, {'id': str(id)})
            record = cursor.fetchall()

            for row in record:
                student = str(row[2])
                selected_il = str(row[0])
                suggestion = str(row[1])

            context = {
                       "id":                id,
                       "course":            cmb_course, 
                       "semester":          cmb_semester, 
                       "student_intervene": student,
                       "selected_il":       selected_il,
                       "il":                il,
                       "suggestion":        suggestion,
                       "user":              request.session['user'], 
                       "role":              request.session['role']}
        
            # *** Plantilla ***
            return render(request, 'preventive_intervention/new_intervention_suggestion.html', context= context)

        ### Eliminar ###
        # Si el botón opción es eliminar
        elif operation[0] == "delete":
            # Se trae el id para eliminar
            id = operation[1]

            # Se consulta el id de courses_semesters
            select = (""" SELECT CS.id 
                        FROM early_intervention.courses_semesters AS CS
                        INNER JOIN early_intervention.courses AS C ON CS.id_course = C.id 
                        INNER JOIN early_intervention.semesters AS S ON CS.id_semester = S.id
                        WHERE C.course_name = %s
                        AND S.semester = %s
                        AND CS.state = 'A' """)
            parameter = (cmb_course, cmb_semester)
            cursor.execute(select, parameter)
            id_courses_semesters = cursor.fetchone()

            # Se actualiza el registro de la tabla intervention_assistance
            update = (""" UPDATE early_intervention.intervention_suggestion 
                          SET state = 'I'
                          WHERE id = %(id_update)s """)
            cursor.execute(update, {'id_update': id})

            # Se cargan las intervenciones con sugerencia
            context = view_intervention_suggestion(request, cmb_course, cmb_semester, id_courses_semesters[0])
        
            # *** Plantilla ***
            return render(request, 'preventive_intervention/list_intervention_suggestion.html', context= context)
            
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
    # Fin validación de variables de sesión
# ***** Fin Operación Intervención Sugerencia *****



# ***** Ver Intervención Sugerencia *****
def view_intervention_suggestion(request, cmb_curso, cmb_semestre, id_courses_semesters):
    # Se genera la conexión con la base de datos
    cursor = connection_postgresql()

    # Se consultan los registros de la tabla
    select = (""" SELECT ISU.id, ISU.suggestion, ISU.students, IA.code, IA.name, ISU.date
                  FROM early_intervention.intervention_suggestion AS ISU
                  INNER JOIN early_intervention.indicator_achievement AS IA ON ISU.id_indicator_achievement = IA.id
                  WHERE ISU.id_courses_semesters = %(id_courses_semesters)s
                  AND ISU.state = 'A' """)
    cursor.execute(select, {'id_courses_semesters': id_courses_semesters})

    record = cursor.fetchall()

    context = {"record":   record, 
               "course":   cmb_curso, 
               "semester": cmb_semestre,
               "user":     request.session['user'], 
               "role":     request.session['role']}

    return context
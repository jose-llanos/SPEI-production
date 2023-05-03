# Se importan las libreria de template
from django.shortcuts import render
# Se importa la librería de tiempo
import datetime

# Se importa la libreria para PostgreSQL
from SPEI.connection import connection_postgresql




# ***** Calificaciones Preventivas *****
def preventive_grade(request):
    # Validación de variables de sesión
    try:
        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'preventive_grade.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Calificaciones Preventivas *****




# ***** Mostrar Calificaciones Preventivas *****
def show_preventive_grade(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        curso = request.POST['cmbCurso']
        semestre = request.POST['cmbSemestre']
        curso_id = curso +"-"+ semestre

        # Se ejecuta el query 
        select = (""" SELECT DISTINCT course_id, student, lab1, lab2
                      FROM early_intervention.classification_data 
                      WHERE course_id = %(cursoid)s
                      ORDER BY student ASC """)
        cursor.execute(select, {'cursoid': curso_id})
     
        registros = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros
        context = {"datos": registros, "usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'preventive_grade.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Mostrar Calificaciones Preventivas  *****



# ***** Calificaciones Proactivas *****
def proactive_grade(request):
    # Validación de variables de sesión
    try:
        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}
        # *** Plantilla ***
        return render(request, 'proactive_grade.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Calificaciones Proactivas *****




# ***** Mostrar Calificaciones Proactivas *****
def show_proactive_grade(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        curso = request.POST['cmbCurso']
        semestre = request.POST['cmbSemestre']

        # Se ejecuta el query 
        select = (""" SELECT * 
                      FROM early_intervention.grades 
                      WHERE course_id = %s AND semester = %s 
                      ORDER BY average ASC""")
        parametros = (curso, semestre)
        cursor.execute(select, parametros)
        
        registros = cursor.fetchall()

        # Se renderiza con el Contexto con los parámetros
        context = {"datos": registros, "usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'proactive_grade.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Mostrar Calificaciones Proactivas  *****




# ***** Buscar Intervención con mensaje *****
'''
def search_intervention_message(request):
    # Validación de variables de sesión
    try:
        context = {"usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'search_intervention_message.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
'''
# ***** Fin Buscar Intervención con mensaje *****




# ***** Reporte Intervención con mensaje *****
def rpt_intervention_message(request):
    # Validación de variables de sesión
    try:
        # Se genera la conexión con la base de datos
        cursor = connection_postgresql()

        # Se utilizan los valores que llegan del formulario
        curso = request.POST['cmbCurso']
        semestre = request.POST['cmbSemestre']
        curso_id = curso +"-"+ semestre

        # Se ejecuta el query para mostrar los registros en el html
        select = (""" SELECT course_id, intervention_date, intervention_topic, 
                      affair, message, students, date
                      FROM early_intervention.intervention_message 
                      WHERE course_id = %(course_id)s""")
        cursor.execute(select, {'course_id': curso_id})

        registros = cursor.fetchall()

        context = {"datos": registros, "usuario": request.session['usuario'], "rol": request.session['rol']}

        # *** Plantilla ***
        return render(request, 'search_intervention_message.html', context= context)
    except KeyError:
        # *** Plantilla ***
        return render(request, 'index.html', context={})
# ***** Fin Reporte Intervención con mensaje *****



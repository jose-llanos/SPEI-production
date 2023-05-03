"""ingesoftware URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path

# views
from SPEI.views import spei
from SPEI.views import main
from SPEI.views import student_dashboard
from SPEI.views import teacher_dashboard
from SPEI.views import sign_off

# search
from SPEI.views_search import preventive_grade
from SPEI.views_search import show_preventive_grade
from SPEI.views_search import proactive_grade
from SPEI.views_search import show_proactive_grade
from SPEI.views_search import rpt_intervention_message

### ----- Package: configuration ----- 

##### views_course #####
from SPEI.app.configuration.views_course import list_course
from SPEI.app.configuration.views_course import new_course
from SPEI.app.configuration.views_course import save_course
from SPEI.app.configuration.views_course import operation_course
##### End views_courses #####

### ----- End Package: configuration ----- 




### ----- Package: preventive_intervention ----- 

##### views_record_preventive_intervention #####
from SPEI.app.preventive_intervention.views_record_preventive_intervention import record_preventive_intervention
from SPEI.app.preventive_intervention.views_record_preventive_intervention import upload_record_preventive_intervention
##### Fin views_record_preventive_intervention #####

##### views_performance_classification #####
from SPEI.app.preventive_intervention.views_performance_classification import performance_classification
from SPEI.app.preventive_intervention.views_performance_classification import performance_classification_prediction
##### Fin views_performance_classification #####

##### views_intervention_suggestion #####
from SPEI.app.preventive_intervention.views_intervention_suggestion import intervention_suggestion
from SPEI.app.preventive_intervention.views_intervention_suggestion import control_intervention_suggestion
from SPEI.app.preventive_intervention.views_intervention_suggestion import upload_suggestion
from SPEI.app.preventive_intervention.views_intervention_suggestion import save_intervention_suggestion
from SPEI.app.preventive_intervention.views_intervention_suggestion import operation_intervention_suggestion
##### End views_intervention_suggestion #####

##### views_intervention_code #####
from SPEI.app.preventive_intervention.views_intervention_code import intervention_code
from SPEI.app.preventive_intervention.views_intervention_code import control_intervention_code
from SPEI.app.preventive_intervention.views_intervention_code import upload_code
from SPEI.app.preventive_intervention.views_intervention_code import save_intervention_code
from SPEI.app.preventive_intervention.views_intervention_code import operation_intervention_code
##### End views_intervention_code #####

##### views_group_tutoring #####
from SPEI.app.preventive_intervention.views_group_tutoring import group_tutoring
from SPEI.app.preventive_intervention.views_group_tutoring import control_group_tutoring
from SPEI.app.preventive_intervention.views_group_tutoring import save_group_tutoring
from SPEI.app.preventive_intervention.views_group_tutoring import operation_group_tutoring
##### End views_group_tutoring #####

##### views_intervention_assistance #####
from SPEI.app.preventive_intervention.views_intervention_assistance import intervention_assistance
from SPEI.app.preventive_intervention.views_intervention_assistance import control_intervention_assistance
from SPEI.app.preventive_intervention.views_intervention_assistance import save_intervention_assistance
from SPEI.app.preventive_intervention.views_intervention_assistance import operation_intervention_assistance
##### End views_intervention_assistance #####

##### views_intervention_assistance_report #####
from SPEI.app.preventive_intervention.views_intervention_assistance_report import intervention_assistance_report
from SPEI.app.preventive_intervention.views_intervention_assistance_report import show_intervention_assistance_report
##### End views_intervention_assistance_report #####

### ----- End Package: preventive_intervention ----- 



### ----- Package: proactive_intervention ----- 

##### views_record_proactive_intervention #####
from SPEI.app.proactive_intervention.views_record_proactive_intervention import record_proactive_intervention
from SPEI.app.proactive_intervention.views_record_proactive_intervention import upload_record_proactive_intervention
##### End views_record_proactive_intervention #####

##### views_performance_regression #####
from SPEI.app.proactive_intervention.views_performance_regression import performance_regression
from SPEI.app.proactive_intervention.views_performance_regression import performance_regression_prediction
##### Fin views_performance_classification #####

##### views_reinforcement #####
from SPEI.app.proactive_intervention.views_reinforcement import reinforcement
from SPEI.app.proactive_intervention.views_reinforcement import student_reinforcement
from SPEI.app.proactive_intervention.views_reinforcement import send_student_reinforcement
##### Fin views_reinforcement #####

##### views_suggestions #####
from SPEI.app.proactive_intervention.views_suggestion import suggestion
from SPEI.app.proactive_intervention.views_suggestion import student_suggestion
##### Fin views_suggestions #####

### ----- Fin Package: proactive_intervention ----- 


### ----- Package: prediction_reports ----- 

##### views_prediction_reports #####
from SPEI.app.prediction_reports.views_prediction_reports import rpt_columns
from SPEI.app.prediction_reports.views_prediction_reports import column_display
from SPEI.app.prediction_reports.views_prediction_reports import rpt_lines
from SPEI.app.prediction_reports.views_prediction_reports import lines_display
##### Fin views_prediction_reports #####

### ----- Fin Package: prediction_reports ----- 


### ----- Package: courses_reports ----- 

##### views_courses_reports #####
from SPEI.app.courses_reports.views_dashboard import activity_grades
from SPEI.app.courses_reports.views_dashboard import display_grades_activity
from SPEI.app.courses_reports.views_dashboard import average_grade
from SPEI.app.courses_reports.views_dashboard import display_average_grade
from SPEI.app.courses_reports.views_dashboard import delivered_activities
from SPEI.app.courses_reports.views_dashboard import display_delivered_activities
from SPEI.app.courses_reports.views_dashboard import tried_activities
from SPEI.app.courses_reports.views_dashboard import display_tried_activities
from SPEI.app.courses_reports.views_dashboard import total_tried
from SPEI.app.courses_reports.views_dashboard import display_total_tried
from SPEI.app.courses_reports.views_dashboard import average_tried_activity
from SPEI.app.courses_reports.views_dashboard import display_average_tried_activity

##### Fin views_courses_reports #####


### ----- Package: performance_reports ----- 

##### views_performance_reports #####
from SPEI.app.performance_reports.views_performance_reports import performance_activity
from SPEI.app.performance_reports.views_performance_reports import display_performance_activity
from SPEI.app.performance_reports.views_performance_reports import weighted_performance
#from SPEI.app.performance_reports.views_performance_reports import display_weighted_performance
### ----- Fin Package: performance_reports ----- 


urlpatterns = [
    #path('admin/', admin.site.urls),
    # views
    path('spei/', spei, name="spei"),
    path('main/', main, name="main"),
    path('student_dashboard/', student_dashboard, name="student_dashboard"),
    path('teacher_dashboard/', teacher_dashboard, name="teacher_dashboard"),
    path('sign_off/', sign_off, name="sign_off"),

    # views_configuracion


    #views_search
    path('preventive_grade/', preventive_grade, name="preventive_grade"),
    path('show_preventive_grade/', show_preventive_grade),
    path('proactive_grade/', proactive_grade, name="proactive_grade"),
    path('show_proactive_grade/', show_proactive_grade),
    path('rpt_intervention_message/', rpt_intervention_message),

    ### ----- Package: configuration ----- 
    
    ##### views_courses #####
    path('list_course/', list_course, name="list_course"),
    path('new_course/', new_course),
    path('save_course/', save_course),
    path('operation_course/', operation_course),
    ##### End views_courses #####

    ### ----- Fin Package: configuration ----- 



    ### ----- Package: preventive_intervention ----- 
   
    ##### views_record_preventive_intervention #####
    path('record_preventive_intervention/', record_preventive_intervention, name="record_preventive_intervention"),
    path('upload_record_preventive_intervention/', upload_record_preventive_intervention),
    ##### End views_record_preventive_intervention #####

    ##### views_performance_classification #####
    path('performance_classification/', performance_classification, name="performance_classification"),
    path('performance_classification_prediction/', performance_classification_prediction),
    ##### Fin views_preventive_intervention #####

    ##### views_intervention_suggestion #####
    path('intervention_suggestion/', intervention_suggestion, name="intervention_suggestion"),
    path('control_intervention_suggestion/', control_intervention_suggestion),
    path('upload_suggestion/', upload_suggestion),
    path('save_intervention_suggestion/', save_intervention_suggestion),
    path('operation_intervention_suggestion/', operation_intervention_suggestion),
    ##### End views_intervention_suggestion #####

    ##### views_intervention_code #####
    path('intervention_code/', intervention_code, name="intervention_code"),
    path('control_intervention_code/', control_intervention_code),
    path('upload_code/', upload_code),
    path('save_intervention_code/', save_intervention_code),
    path('operation_intervention_code/', operation_intervention_code),
    ##### End views_intervention_code #####

    ##### views_group_tutoring #####
    path('group_tutoring/', group_tutoring, name="group_tutoring"),
    path('control_group_tutoring/', control_group_tutoring),
    path('save_group_tutoring/', save_group_tutoring),
    path('operation_group_tutoring/', operation_group_tutoring),
    ##### End views_group_tutoring #####

    ##### views_intervention_assistance #####
    path('intervention_assistance/', intervention_assistance, name="intervention_assistance"),
    path('control_intervention_assistance/', control_intervention_assistance),
    path('save_intervention_assistance/', save_intervention_assistance),
    path('operation_intervention_assistance/', operation_intervention_assistance),
    ##### End views_intervention_assistance #####

    ##### views_intervention_assistance_report #####
    path('intervention_assistance_report/', intervention_assistance_report, name="intervention_assistance_report"),
    path('show_intervention_assistance_report/', show_intervention_assistance_report),
    ##### End views_intervention_assistance_report #####

    ### ----- Fin Package: preventive_intervention ----- 




    ### ----- Package: proactive_intervention ----- 

    ##### views_record_proactive_intervention #####
    path('record_proactive_intervention/', record_proactive_intervention, name="record_proactive_intervention"),
    path('upload_record_proactive_intervention/', upload_record_proactive_intervention),
    ##### Fin views_record_proactive_intervention #####

    ##### views_performance_regression #####
    path('performance_regression/', performance_regression, name="performance_regression"),
    path('performance_regression_prediction/', performance_regression_prediction),
    ##### Fin views_preventive_regression #####

    ##### views_reinforcement #####
    path('reinforcement/', reinforcement, name="reinforcement"),
    path('student_reinforcement/', student_reinforcement),
    path('send_student_reinforcement/', send_student_reinforcement),
    ##### Fin views_reinforcement #####

    ##### views_suggestion #####
    path('suggestion/', suggestion, name="suggestion"),
    path('student_suggestion/', student_suggestion),
    ##### Fin views_suggestions #####


    ### ----- Fin Package: proactive_intervention ----- 
   

    
    ### ----- Package: prediction_reports ----- 

    ##### views_prediction_reports #####
    path('rpt_columns/', rpt_columns, name="rpt_columns"),
    path('column_display/', column_display),
    path('rpt_lines/', rpt_lines, name="rpt_lines"),
    path('lines_display/', lines_display),
    ##### Fin views_prediction_reports #####

    ### ----- Fin Package: prediction_reports ----- 



    ### ----- Package: courses_reports ----- 

    ##### views_courses_reports #####
    path('activity_grades/', activity_grades, name="activity_grades"),
    path('display_grades_activity/', display_grades_activity),
    path('average_grade/', average_grade, name="average_grade"),
    path('display_average_grade/', display_average_grade),
    path('delivered_activities/', delivered_activities, name="delivered_activities"),
    path('display_delivered_activities/', display_delivered_activities),
    path('tried_activities/', tried_activities, name="tried_activities"),
    path('display_tried_activities/', display_tried_activities),
    path('total_tried/', total_tried, name="total_tried"),
    path('display_total_tried/', display_total_tried),
    path('average_tried_activity/', average_tried_activity, name="average_tried_activity"),
    path('display_average_tried_activity/', display_average_tried_activity),
    ##### Fin views_courses_reports #####


    ### ----- Fin Package: courses_reports ----- 




    ### ----- Package: performance_reports ----- 

    ##### views_performance_reports #####
    path('performance_activity/', performance_activity, name="performance_activity"),
    path('display_performance_activity/', display_performance_activity),
    path('weighted_performance/', weighted_performance, name="weighted_performance"),
    #path('display_weighted_performance/', display_weighted_performance),

    ### ----- Fin Package: performance_reports ----- 
    
]

from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # AUTH
    # =========================
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # =========================
    # DASHBOARD
    # =========================
    path('generate/', views.generate_view, name='generate'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    # =========================
    # TIMETABLE
    # =========================
    path('timetable/', views.timetable_view, name='timetable'),
    #path('download-pdf/', views.download_pdf, name='download_pdf'),

    # =========================
    # ADD DATA (ADMIN)
    # =========================
    path('add-department/', views.add_department, name='add_department'),
    path('add-semester/', views.add_semester, name='add_semester'),
    path('add-faculty/', views.add_faculty, name='add_faculty'),
    path('add-subject/', views.add_subject, name='add_subject'),
    path('assign-subject/', views.add_subject_faculty, name='add_subject_faculty'),
    path('add-classroom/', views.add_classroom, name='add_classroom'),
    path('add-timeslot/', views.add_timeslot, name='add_timeslot'),
    
    #Delete Faculty
    path('delete-faculty/<int:id>/', views.delete_faculty, name='delete_faculty'),
    
]
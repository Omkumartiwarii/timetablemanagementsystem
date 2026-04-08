from django.urls import path
from . import views

urlpatterns = [
    # LOGIN PAGE (HOMEPAGE)
    path('', views.login_view, name='login'),

    # ADMIN
    path('generate/', views.generate_view, name='generate'),
    #path('admin_dashboard/', views.generate_view, name='admin_dashboard'),

    # STUDENT
    path('student/', views.student_dashboard, name='student_dashboard'),

    # TIMETABLE
    path('timetable/', views.timetable_view, name='timetable'),

    # PDF
    path('download/', views.download_pdf, name='download'),

    # LOGOUT
    path('logout/', views.logout_view, name='logout'),
]
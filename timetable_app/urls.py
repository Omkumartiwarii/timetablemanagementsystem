from django.urls import path, include
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
    path('faculty-dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),

    # =========================
    # TIMETABLE
    # =========================
    path('timetable/', views.timetable_view, name='timetable'),
    # That duplicate was overriding timetable_view and breaking Add/Edit/Delete

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
    path('generate/', views.generate_view, name='generate'),
    path('teams/', views.teams_page, name='teams'),
    
    # Delete
    path('delete-faculty/<int:id>/', views.delete_faculty, name='delete_faculty'),
    path('delete-classroom/<int:id>/', views.delete_classroom, name='delete_classroom'),
    path('delete-department/<int:id>/', views.delete_department, name='delete_department'),
    path('delete-semester/<int:id>/', views.delete_semester, name='delete_semester'),
    path('delete-subject/<int:id>/', views.delete_subject, name='delete_subject'),
    path('delete-subject-faculty/<int:id>/', views.delete_subject_faculty, name='delete_subject_faculty'),
    path('delete-timeslot/<int:id>/', views.delete_timeslot, name='delete_timeslot'),
    path('remove-timetable/', views.remove_timetable, name='remove_timetable'),
    
    # Clear Recent Actions
    path('clear-recent-activities/', views.clear_recent_activities, name='clear_recent_activities'),
    
    # ✅ Add/Edit/Delete timetable entries (AJAX)
    path('timetable/get/<int:id>/', views.get_timetable_entry, name='get_timetable_entry'),
    path('timetable/save/', views.save_timetable_entry, name='save_timetable_entry'),
    path('timetable/delete/<int:id>/', views.delete_timetable_entry, name='delete_timetable_entry'),
    
    #ChatBot
    path(
    'ttgs-ai-chat/',
    views.ttgs_ai_chat,
    name='ttgs_ai_chat'
),
]
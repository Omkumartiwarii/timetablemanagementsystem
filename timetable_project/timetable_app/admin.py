from django.contrib import admin

# Register your models here.

from .models import (
    Department,
    Semester,
    Faculty,
    Subject,
    SubjectFaculty,
    Classroom,
    TimeSlot,
    Timetable
)

# =========================
# Department
# =========================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


# =========================
# Semester
# =========================
@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'department', 'semester_number']
    list_filter = ['department']


# =========================
# Faculty
# =========================
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department']
    list_filter = ['department']
    search_fields = ['name']


# =========================
# Subject
# =========================
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'semester']
    list_filter = ['semester']
    search_fields = ['name']


# =========================
# Subject-Faculty Mapping
# =========================
@admin.register(SubjectFaculty)
class SubjectFacultyAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'faculty']
    list_filter = ['subject', 'faculty']


# =========================
# Classroom
# =========================
@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['id', 'room_number', 'capacity']
    search_fields = ['room_number']


# =========================
# TimeSlot
# =========================
@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['id', 'day', 'start_time', 'end_time']
    list_filter = ['day']


# =========================
# Timetable
# =========================
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['id', 'semester', 'subject', 'faculty', 'classroom', 'timeslot']
    list_filter = ['semester', 'faculty', 'classroom']
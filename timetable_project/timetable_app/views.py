from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .algorithms import generate_timetable
import io

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from .algorithms import generate_timetable

# =========================
# LOGIN
# =========================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 ROLE-BASED REDIRECTION
            if user.is_staff:
                return redirect('generate')   # Admin Dashboard
            else:
                return redirect('student_dashboard')  # Student Dashboard

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# ADMIN: GENERATE TIMETABLE
# =========================
@login_required
def generate_view(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')

    semesters = Semester.objects.all()
    departments = Department.objects.all()

    if request.method == 'POST':
        semester_id = request.POST.get('semester')
        semester = get_object_or_404(Semester, id=semester_id)

        Timetable.objects.filter(semester=semester).delete()

        schedule = generate_timetable(semester)

        for entry in schedule:
            Timetable.objects.create(
                semester=semester,
                subject=entry['subject'],
                faculty=entry['faculty'],
                classroom=entry['classroom'],
                timeslot=entry['slot']
            )

        return redirect(f'/timetable/?semester={semester.id}')

    return render(request, 'admin_dashboard.html', {
        'semesters': semesters,
        'departments': departments
    })

# =========================
# VIEW TIMETABLE
# =========================
@login_required
def timetable_view(request):
    semester_id = request.GET.get('semester')
    department_id = request.GET.get('department')

    data = Timetable.objects.all()

    # ✅ Filter by semester
    if semester_id:
        data = data.filter(semester_id=semester_id)

    # ✅ Filter by department (via semester relation)
    if department_id:
        data = data.filter(semester__department_id=department_id)

    # Order properly
    timetable = data.order_by('timeslot__day', 'timeslot__start_time')

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    slots = TimeSlot.objects.values('start_time', 'end_time').distinct().order_by('start_time')

    return render(request, 'timetable.html', {
        'timetable': timetable,
        'days': days,
        'slots': slots,
        'semesters': Semester.objects.all(),
        'departments': Department.objects.all(),
        'selected_semester': semester_id,
        'selected_department': department_id
    })
# =========================
# STUDENT DASHBOARD
# =========================
@login_required
def student_dashboard(request):
    semesters = Semester.objects.all()
    departments = Department.objects.all()

    data = Timetable.objects.all()

    semester_id = request.GET.get('semester')
    department_id = request.GET.get('department')

    if semester_id:
        data = data.filter(semester_id=semester_id)

    if department_id:
        data = data.filter(semester__department_id=department_id)

    return render(request, 'student_dashboard.html', {
        'data': data,
        'semesters': semesters,
        'departments': departments
    })


# =========================
# DOWNLOAD PDF
# =========================
@login_required
def download_pdf(request):
    semester_id = request.GET.get('semester')

    if semester_id:
        data = Timetable.objects.filter(semester_id=semester_id)
    else:
        data = Timetable.objects.all()

    data = data.order_by('timeslot__day', 'timeslot__start_time')

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    table_data = [["Day", "Time", "Subject", "Faculty", "Room"]]

    for t in data:
        table_data.append([
            t.timeslot.day,
            f"{t.timeslot.start_time}-{t.timeslot.end_time}",
            t.subject.name,
            t.faculty.name,
            t.classroom.room_number
        ])

    table = Table(table_data)

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    doc.build([table])   

    buffer.seek(0)

    return HttpResponse(
        buffer,
        content_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=\"timetable.pdf\"'}
    )
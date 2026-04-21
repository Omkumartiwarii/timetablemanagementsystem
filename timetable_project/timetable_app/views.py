from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import *   # ✅ FIXED (top pe)
from .algorithms import generate_timetable
import io

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


# =========================
# LOGIN
# =========================
def login_view(request):
    from django.contrib.auth.models import User

    if request.method == 'POST':
        role = request.POST.get('role')

        # ================= ADMIN LOGIN =================
        if role == "admin":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user and user.is_staff:
                login(request, user)
                return redirect('generate')
            else:
                messages.error(request, "Invalid Admin Credentials")

        # ================= STUDENT DIRECT LOGIN =================
        elif role == "student":
            enrollment = request.POST.get('enrollment')

            if enrollment:
                user, created = User.objects.get_or_create(username=enrollment)
            else:
                user, created = User.objects.get_or_create(username="guest_student")

            user.set_unusable_password()
            user.save()

            login(request, user)
            return redirect('student_dashboard')

    return render(request, 'login.html')


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect('login')


# =========================
# GENERATE TIMETABLE
# =========================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def generate_view(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')

    semesters = Semester.objects.all()
    departments = Department.objects.all()

    auto = request.GET.get('auto')

    def generate_for_semesters(sem_list):
        for sem in sem_list:
            print(f"Generating for: {sem}")

            Timetable.objects.filter(semester=sem).delete()

            schedule = generate_timetable(sem)
            print("Schedule:", schedule)

            if not schedule:
                print("No schedule generated!")
                continue

            for entry in schedule:
                try:
                    Timetable.objects.create(
                        semester=sem,
                        subject=entry.get('subject'),
                        faculty=entry.get('faculty'),
                        classroom=entry.get('classroom'),
                        timeslot=entry.get('slot')  # change if needed
                    )
                except Exception as e:
                    print("Save Error:", e)

    # AUTO GENERATE
    if auto:
        generate_for_semesters(Semester.objects.all())
        messages.success(request, "Timetable Generated Successfully ✅")
        return redirect('timetable')

    # POST LOGIC
    if request.method == 'POST':
        semester_id = request.POST.get('semester')
        department_id = request.POST.get('department')

        if semester_id == "all":
            if department_id != "all":
                sems = Semester.objects.filter(department_id=department_id)
            else:
                sems = Semester.objects.all()

            generate_for_semesters(sems)
            return redirect('timetable')

        if department_id == "all":
            generate_for_semesters(Semester.objects.all())
            return redirect('timetable')

        semester = get_object_or_404(Semester, id=semester_id)
        generate_for_semesters([semester])

        return redirect(f'/timetable/?semester={semester.id}')

    return render(request, 'admin_dashboard.html', {
        'semesters': semesters,
        'departments': departments,
        'faculties': Faculty.objects.all(),
        'subjects': Subject.objects.all(),
    })

# =========================
# VIEW TIMETABLE
# =========================
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Timetable, TimeSlot, Semester, Department


@login_required
def timetable_view(request):
    semester_id = request.GET.get('semester')
    department_id = request.GET.get('department')

    # ✅ optimized query
    data = Timetable.objects.select_related(
        'subject',
        'faculty',
        'classroom',
        'semester__department',
        'timeslot'
    )

    # ✅ filters
    if semester_id and semester_id != "all":
        data = data.filter(semester_id=semester_id)

    if department_id and department_id != "all":
        data = data.filter(semester__department_id=department_id)

    # ✅ grouping + unique slot mapping
    grouped_data = {}

    for entry in data:
        dept_name = entry.semester.department.name
        sem_name = f"Semester {entry.semester.semester_number}"
        key = f"{dept_name} - {sem_name}"

        if key not in grouped_data:
            grouped_data[key] = {}

        # 🔥 IMPORTANT (format match)
        slot_key = f"{entry.timeslot.day}_{entry.timeslot.start_time.strftime('%H:%M')}"
        grouped_data[key][slot_key] = entry

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    slots = TimeSlot.objects.values('start_time', 'end_time') \
                            .distinct() \
                            .order_by('start_time')

    return render(request, 'timetable.html', {
        'grouped_data': grouped_data,
        'days': days,
        'slots': slots,
        'semesters': Semester.objects.all(),
        'departments': Department.objects.all(),
        'selected_semester': semester_id or "all",
        'selected_department': department_id or "all"
    })


# =========================
# STUDENT DASHBOARD
# =========================
from django.shortcuts import render
from .models import *

def student_dashboard(request):
    departments = Department.objects.all()
    semesters = Semester.objects.select_related('department')

    # ✅ PROPER UNIQUE TIMESLOTS (no duplicates)
    slots = TimeSlot.objects.order_by('start_time', 'end_time')
    unique_slots = []
    seen = set()

    for slot in slots:
        key = (slot.start_time, slot.end_time)
        if key not in seen:
            seen.add(key)
            unique_slots.append(slot)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    selected_department = request.GET.get('department')
    selected_semester = request.GET.get('semester')

    timetable_qs = Timetable.objects.select_related(
        'subject', 'faculty', 'classroom', 'timeslot', 'semester__department'
    )

    # ✅ FILTERS
    if selected_department and selected_department != "all":
        timetable_qs = timetable_qs.filter(
            semester__department_id=selected_department
        )

    if selected_semester and selected_semester != "all":
        timetable_qs = timetable_qs.filter(
            semester_id=selected_semester
        )

    # ✅ GROUPING LOGIC
    grouped_data = {}

    for entry in timetable_qs:
        title = f"{entry.semester.department.name} - Sem {entry.semester.semester_number}"

        if title not in grouped_data:
            grouped_data[title] = {}

        key = f"{entry.timeslot.day}_{entry.timeslot.start_time.strftime('%H:%M')}"
        grouped_data[title][key] = entry

    return render(request, 'student_dashboard.html', {
        'departments': departments,
        'semesters': semesters,
        'slots': unique_slots,  # ✅ FIXED
        'days': days,
        'grouped_data': grouped_data,

        # ✅ IMPORTANT (dropdown selected value maintain karega)
        'selected_department': selected_department,
        'selected_semester': selected_semester,
    })


# =========================
# DOWNLOAD PDF
# =========================
# @login_required
# def download_pdf(request):
#     semester_id = request.GET.get('semester')

#     if semester_id:
#         data = Timetable.objects.filter(semester_id=semester_id)
#     else:
#         data = Timetable.objects.all()

#     data = data.order_by('timeslot__day', 'timeslot__start_time')

#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer)

#     table_data = [["Day", "Time", "Subject", "Faculty", "Room"]]

#     for t in data:
#         table_data.append([
#             t.timeslot.day,
#             f"{t.timeslot.start_time}-{t.timeslot.end_time}",
#             t.subject.name,
#             t.faculty.name,
#             t.classroom.room_number
#         ])

#     table = Table(table_data)

#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     doc.build([table])
#     buffer.seek(0)

#     return HttpResponse(
#         buffer,
#         content_type='application/pdf',
#         headers={'Content-Disposition': 'attachment; filename="timetable.pdf"'}
#     )


# =========================
# ADD DATA (ADMIN ONLY)
# =========================

#Add & View Department
@login_required
def add_department(request):
    show_list = False

    # ✅ View button (GET)
    if request.GET.get("view_list") == "true":
        show_list = True

    # ✅ Save department
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            Department.objects.create(name=name)
            return redirect('add_department')

    return render(request, 'add_department.html', {
        # ✅ counts (fast + safe)
        'departments': Department.objects.count(),
        'semesters': Semester.objects.count(),
        'faculties': Faculty.objects.count(),
        'subjects': Subject.objects.count(),

        # ✅ list show
        'dept_list': Department.objects.all() if show_list else None,
    })


@login_required
def add_semester(request):
    form = SemesterForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('add_semester')

    return render(request, 'add_semester.html', {
        'form': form,

        # stats
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
        'faculties': Faculty.objects.all(),
        'subjects': Subject.objects.all(),
    })

#Add & View faculty
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Faculty, Department, Semester, Subject
from .forms import FacultyForm
from django.shortcuts import get_object_or_404


@login_required
def delete_faculty(request, id):
    faculty = get_object_or_404(Faculty, id=id)
    faculty.delete()
    return redirect('/add_faculty/?view_list=true')

@login_required
def add_faculty(request):
    form = FacultyForm(request.POST or None)

    show_list = False

    # ✅ GET request handle karo
    if request.GET.get("view_list") == "true":
        show_list = True

    # ✅ SAVE handle
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('add_faculty')

    return render(request, 'add_faculty.html', {
        'form': form,
        'title': 'Add Faculty',
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
        'subjects': Subject.objects.all(),
        'faculties_count': Faculty.objects.count(),
        'faculties': Faculty.objects.all() if show_list else None,
    })


def add_subject(request):
    form = SubjectForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('add_subject')

    return render(request, 'add_subject.html', {
        'form': form,

        # 👇 IMPORTANT stats ke liye
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
        'faculties': Faculty.objects.all(),
        'subjects': Subject.objects.all(),
    })


@login_required
def add_subject_faculty(request):
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        faculty_id = request.POST.get('faculty')

        SubjectFaculty.objects.create(
            subject_id=subject_id,
            faculty_id=faculty_id
        )
        return redirect('add_subject_faculty')

    return render(request, 'add_subject_faculty.html', {
        'subjects': Subject.objects.all(),
        'faculties': Faculty.objects.all(),

        # stats
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
    })


@login_required
def add_classroom(request):
    form = ClassroomForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('add_classroom')

    return render(request, 'add_classroom.html', {
        'form': form,

        # stats ke liye
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
        'faculties': Faculty.objects.all(),
        'classrooms': Classroom.objects.all(),
    })


#Add & View TimeSlot
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TimeSlot, Department, Semester, Faculty, Subject
from .forms import TimeSlotForm

@login_required
def add_timeslot(request):
    form = TimeSlotForm(request.POST or None)

    show_list = False

    # ✅ GET request se list show
    if request.GET.get("view_list") == "true":
        show_list = True

    # ✅ SAVE
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('add_timeslot')

    return render(request, 'add_timeslot.html', {
        'form': form,
        'title': 'Add Time Slot',

        # ✅ stats
        'departments': Department.objects.count(),
        'semesters': Semester.objects.count(),
        'faculties': Faculty.objects.count(),
        'subjects': Subject.objects.count(),

        # ✅ list
        'timeslots': TimeSlot.objects.all() if show_list else None,
    })

# Add Faculty
# def add_faculty(request):
#     if request.method == "POST":
#         form = FacultyForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('add_faculty')  # reload page after save
#     else:
#         form = FacultyForm()

#     return render(request, 'add_faculty.html', {'form': form})
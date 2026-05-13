# views.py — Cleaned & Fixed
# =====================================================
# All duplicate imports removed, logic organized
# =====================================================

import io
from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from reportlab.lib import colors
from django.db import models
from django.utils.timezone import now
from .models import RecentActivity

from .models import (
    Department,
    Semester,
    Faculty,
    Subject,
    SubjectFaculty,
    Classroom,
    TimeSlot,
    Timetable,
    #SubjectLabRoom,
    RecentActivity,
)
from .forms import (
    FacultyForm,
    SemesterForm,
    SubjectForm,
    ClassroomForm,
    TimeSlotForm,
)
# from .algorithms import generate_all_timetables, generate_timetable

from .algorithms import generate_all_timetables, generate_timetable,assign_preferred_classrooms

# =========================
# HOME
# =========================
def home(request):
    return render(request, 'home.html')


# =========================
# LOGIN
# =========================
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')

        # -------- ADMIN LOGIN --------
        if role == "admin":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid Admin Credentials")

        # -------- FACULTY LOGIN --------
        elif role == "faculty":
            username = request.POST.get('faculty_username')
            password = request.POST.get('faculty_password')

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user:
                login(request, user)
                return redirect('faculty_dashboard')
            else:
                messages.error(request, "Invalid Faculty Credentials")

        # -------- STUDENT LOGIN --------
        elif role == "student":
            enrollment = request.POST.get('enrollment', '').strip()

            username = enrollment if enrollment else "guest_student"

            user, created = User.objects.get_or_create(
                username=username
            )

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
# ADMIN DASHBOARD
# =========================

@login_required
def admin_dashboard(request):

    if request.method == "POST" and 'save_all' in request.POST:

        # =========================
        # DEPARTMENT
        # =========================

        department_name = request.POST.get(
            'department_name',
            ''
        ).strip()

        if department_name:

            department = Department.objects.create(
                name=department_name
            )

            # RECENT ACTIVITY

            RecentActivity.objects.create(
                title=f"Added new department {department.name}",
                action_type='Department'
            )

        # =========================
        # FACULTY
        # =========================

        faculty_form = FacultyForm(request.POST)

        if request.POST.get('name') and faculty_form.is_valid():

            faculty = faculty_form.save()

            # RECENT ACTIVITY

            RecentActivity.objects.create(
                title=f"Added new faculty {faculty.name}",
                action_type='Faculty'
            )

        # =========================
        # SEMESTER
        # =========================

        semester_form = SemesterForm(request.POST)

        if request.POST.get('semester_name') and semester_form.is_valid():

            semester = semester_form.save()

            # RECENT ACTIVITY

            RecentActivity.objects.create(
                title=f"Added new semester {semester}",
                action_type='Semester'
            )

        # =========================
        # SUBJECT FACULTY
        # =========================

        subject_id = request.POST.get('subject')

        faculty_id = request.POST.get('faculty')

        if subject_id and faculty_id:

            assignment, created = SubjectFaculty.objects.get_or_create(
                subject_id=subject_id,
                faculty_id=faculty_id
            )

            if created:

                # RECENT ACTIVITY

                RecentActivity.objects.create(
                    title=f"Assigned {assignment.subject.name} to {assignment.faculty.name}",
                    action_type='Subject Faculty'
                )

        return redirect('admin_dashboard')

    context = {

        'faculty_form': FacultyForm(),

        'semester_form': SemesterForm(),

        'subjects': Subject.objects.all(),

        'faculties': Faculty.objects.all(),

        'departments': Department.objects.all(),

        'semesters': Semester.objects.all(),

        # RECENT ACTIVITIES

        'recent_activities': RecentActivity.objects.all().order_by(
            '-created_at'
        )[:10],
    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )


# =========================
# CLEAR RECENT ACTIVITIES
# =========================

@login_required
def clear_recent_activities(request):

    if request.method == "POST":

        RecentActivity.objects.all().delete()

    return redirect('admin_dashboard')



# =========================
# FACULTY DASHBOARD
# =========================
# REPLACE YOUR views.py WITH THIS

from django.shortcuts import render
from datetime import datetime
from .models import Faculty, Timetable, Subject

DAY_ORDER = [
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
]


def faculty_dashboard(request):

    faculty_id = request.GET.get('faculty')

    faculty = None
    today_timetable = []
    week_timetable = []
    subjects = []

    all_faculties = Faculty.objects.all()

    current_day = datetime.today().strftime('%A')

    if faculty_id:

        faculty = Faculty.objects.filter(
            id=faculty_id
        ).first()

        if faculty:

            # TODAY TIMETABLE
            today_qs = Timetable.objects.filter(
                faculty__id=faculty.id,
                timeslot__day=current_day
            ).select_related(
                'timeslot',
                'subject',
                'semester',
                'classroom'
            ).order_by(
                'timeslot__start_time'
            )

            # TODAY TIME FORMAT
            for item in today_qs:

                item.start = item.timeslot.start_time.strftime(
                    "%I:%M %p"
                )

                item.end = item.timeslot.end_time.strftime(
                    "%I:%M %p"
                )

            today_timetable = today_qs

            # WEEK TIMETABLE
            week_qs = Timetable.objects.filter(
                faculty__id=faculty.id
            ).select_related(
                'timeslot',
                'subject',
                'semester',
                'classroom'
            )

            # WEEK TIME FORMAT
            for item in week_qs:

                item.start = item.timeslot.start_time.strftime(
                    "%I:%M %p"
                )

                item.end = item.timeslot.end_time.strftime(
                    "%I:%M %p"
                )

            # CUSTOM DAY SORT
            week_timetable = sorted(
                week_qs,
                key=lambda x: (
                    DAY_ORDER.index(x.timeslot.day)
                    if x.timeslot.day in DAY_ORDER
                    else 99,
                    x.timeslot.start_time
                )
            )

            # SUBJECTS
            subjects = Subject.objects.filter(
                subjectfaculty__faculty=faculty
            ).distinct()

    context = {
        'faculty': faculty,
        'today_timetable': today_timetable,
        'week_timetable': week_timetable,
        'subjects': subjects,
        'all_faculties': all_faculties,
    }

    return render(
        request,
        'faculty_dashboard.html',
        context
    )

# =========================
# GENERATE TIMETABLE
# =========================

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import (
    Department,
    Semester,
    Timetable,
    RecentActivity,
)

from .algorithms import (
    generate_all_timetables,
    # generate_department_timetable,
    # generate_single_semester_timetable,
)


@login_required
def generate_view(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')

    departments = Department.objects.all()
    semesters = Semester.objects.all().order_by('department', 'semester_number')

    if request.method == "POST":
        generate_type = request.POST.get('generate_type')
        department_id = request.POST.get('department')
        semester_id = request.POST.get('semester')

        try:
            if generate_type == "all":
                Timetable.objects.all().delete()
                generate_all_timetables(semesters)
                messages.success(request, "All timetables generated successfully.")

            elif generate_type == "department":
                department = get_object_or_404(Department, id=department_id)
                department_semesters = Semester.objects.filter(department=department)
                Timetable.objects.filter(semester__department=department).delete()
                # fetch theory rooms once
                theory_rooms = list(Classroom.objects.filter(is_lab=False))
                # create preferred room mapping
                preferred_map = assign_preferred_classrooms(department_semesters,theory_rooms)
                for sem in department_semesters:
                    pref = preferred_map.get(sem.id, {})
                    generate_timetable(sem,pref,theory_rooms)
                messages.success(request, f"{department.name} timetable regenerated.")

            elif generate_type == "semester":
                semester = get_object_or_404(Semester, id=semester_id)
                Timetable.objects.filter(semester=semester).delete()
                # fetch theory rooms
                theory_rooms = list(Classroom.objects.filter(is_lab=False))
                # create preferred mapping
                preferred_map = assign_preferred_classrooms(
                    [semester],
                    theory_rooms
                )
                pref = preferred_map.get(semester.id, {})
                generate_timetable(semester,pref,theory_rooms)
                messages.success(request, f"{semester} timetable regenerated.")

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'generate.html', {
        'departments': departments,
        'semesters': semesters,
    })
    
    
# =========================
# REMOVE TIMETABLE
# =========================

from django.contrib import messages
from django.shortcuts import render, redirect

from .models import (
    Timetable,
    Semester,
    Department,
    RecentActivity
)

def remove_timetable(request):

    departments = Department.objects.all()

    semesters = Semester.objects.all().order_by(
        'department',
        'semester_number'
    )

    if request.method == "POST":

        remove_type = request.POST.get('remove_type')
        department_id = request.POST.get('department')
        semester_id = request.POST.get('semester')

        # ================= REMOVE ALL =================

        if remove_type == "all":

            Timetable.objects.all().delete()

            # RECENT ACTIVITY

            RecentActivity.objects.create(
                title="Removed all timetables successfully",
                action_type='Remove'
            )

            messages.success(
                request,
                "All timetable deleted successfully."
            )

        # ================= REMOVE DEPARTMENT =================

        elif remove_type == "department" and department_id:

            department = Department.objects.get(
                id=department_id
            )

            Timetable.objects.filter(
                semester__department_id=department_id
            ).delete()

            # RECENT ACTIVITY

            RecentActivity.objects.create(
                title=f"Removed timetable for {department.name} department",
                action_type='Remove'
            )

            messages.success(
                request,
                "Department timetable deleted successfully."
            )

        # ================= REMOVE SEMESTER =================

        elif remove_type == "semester" and semester_id:

            semester = Semester.objects.get(
                id=semester_id
            )

            Timetable.objects.filter(
                semester_id=semester_id
            ).delete()

            # RECENT ACTIVITY

            RecentActivity.objects.create(
                title=f"Removed timetable for {semester}",
                action_type='Remove'
            )

            messages.success(
                request,
                "Semester timetable deleted successfully."
            )

        return redirect('remove_timetable')

    context = {
        'departments': departments,
        'semesters': semesters,
    }

    return render(
        request,
        'remove_timetable.html',
        context
    )

# =========================
# IMPORTS
# =========================
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import (
    Timetable,
    Semester,
    Department,
    Faculty,
    Subject,
    TimeSlot,
)


# =========================
# VIEW TIMETABLE (Admin)
# =========================
@login_required
def timetable_view(request):

    import json

    semester_id = request.GET.get('semester', 'all')
    department_id = request.GET.get('department', 'all')

    data = Timetable.objects.select_related(
        'subject',
        'classroom',
        'semester__department',
        'timeslot'
    ).prefetch_related('faculty')

    # =========================
    # Prevent Department / Semester Mismatch
    # =========================
    if department_id != "all" and semester_id != "all":

        try:
            sem = Semester.objects.get(id=semester_id)

            if str(sem.department_id) != str(department_id):
                semester_id = "all"

        except Semester.DoesNotExist:
            semester_id = "all"

    # =========================
    # Department Filter
    # =========================
    if department_id != "all":

        data = data.filter(
            semester__department_id=int(department_id)
        )

    # =========================
    # Semester Filter
    # =========================
    if semester_id != "all":

        data = data.filter(
            semester_id=int(semester_id)
        )

    # =========================
    # GROUP TIMETABLE DATA
    # =========================
    grouped_data = {}

    for entry in data:

        key = (
            f"{entry.semester.department.name} - "
            f"Semester {entry.semester.semester_number}"
        )

        if key not in grouped_data:
            grouped_data[key] = {}

        slot_key = (
            f"{entry.timeslot.day}_"
            f"{entry.timeslot.start_time.strftime('%H:%M')}"
        )

        grouped_data[key][slot_key] = entry

    # =========================
    # DAYS & SLOTS
    # =========================
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    slots = TimeSlot.objects.values(
        'start_time',
        'end_time',
        'is_break'
    ).distinct().order_by('start_time')

    # =========================
    # TODAY NAME
    # =========================
    today_name = datetime.today().strftime('%A')

    if today_name not in days:
        today_name = "Monday"

    # =========================
    # ALL WEEK SCHEDULE JSON
    # =========================
    WEEK = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
    ]

    all_schedules = {}

    for day in WEEK:

        entries = Timetable.objects.filter(
            timeslot__day=day
        ).select_related(
            'semester',
            'subject',
            'classroom',
            'timeslot'
        ).prefetch_related(
            'faculty'
        ).order_by(
            'timeslot__start_time'
        )

        day_items = []

        for entry in entries:

            day_items.append({

                "subject": entry.subject.name,

                "time": (
                    f"{entry.timeslot.start_time.strftime('%I:%M %p')} - "
                    f"{entry.timeslot.end_time.strftime('%I:%M %p')}"
                ),

                "semester": (
                    f"{entry.semester.department.name} "
                    f"Sem {entry.semester.semester_number}"
                ),

                "room": entry.classroom.room_number,

                "faculty": ", ".join(
                    f.name for f in entry.faculty.all()
                ) or "Not Assigned",
            })

        all_schedules[day] = day_items

    # =========================
    # RENDER
    # =========================
    return render(request, 'timetable.html', {

        # TIMETABLE
        'grouped_data': grouped_data,

        # FILTERS
        'departments': Department.objects.all(),

        'semesters': Semester.objects.all().order_by(
            'department',
            'semester_number'
        ),

        # STATS
        'faculties': Faculty.objects.all(),
        'subjects': Subject.objects.all(),

        # TABLE
        'days': days,
        'slots': slots,

        # SELECTED FILTERS
        'selected_semester': semester_id,
        'selected_department': department_id,

        # TODAY SECTION
        'today_name': today_name,

        # JSON DATA
        'all_schedules_json': json.dumps(all_schedules),
    })


# =========================
# STUDENT DASHBOARD
# =========================
def student_dashboard(request):
    selected_department = request.GET.get('department', 'all')
    selected_semester = request.GET.get('semester', 'all')

    # Unique time slots (no duplicates)
    slots_qs = TimeSlot.objects.order_by('start_time', 'end_time')
    unique_slots = []
    seen = set()
    for slot in slots_qs:
        key = (slot.start_time, slot.end_time)
        if key not in seen:
            seen.add(key)
            unique_slots.append(slot)

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Prevent mismatch
    if selected_department != "all" and selected_semester != "all":
        try:
            sem = Semester.objects.get(id=selected_semester)
            if str(sem.department_id) != str(selected_department):
                selected_semester = "all"
        except Semester.DoesNotExist:
            selected_semester = "all"

    # Semester dropdown based on department
    if selected_department != "all":
        semesters = Semester.objects.filter(department_id=selected_department)
    else:
        semesters = Semester.objects.select_related('department')

    # Timetable query
    timetable_qs = Timetable.objects.select_related(
        'subject', 'classroom', 'timeslot', 'semester__department'
    ).prefetch_related('faculty')

    if selected_department != "all":
        timetable_qs = timetable_qs.filter(semester__department_id=selected_department)

    if selected_semester != "all":
        timetable_qs = timetable_qs.filter(semester_id=selected_semester)

    # Group entries
    grouped_data = {}
    for entry in timetable_qs:
        title = f"{entry.semester.department.name} - Sem {entry.semester.semester_number}"
        if title not in grouped_data:
            grouped_data[title] = {}
        key = f"{entry.timeslot.day}_{entry.timeslot.start_time.strftime('%H:%M')}"
        grouped_data[title][key] = entry

    return render(request, 'student_dashboard.html', {
        'departments': Department.objects.all(),
        'semesters': semesters,
        'slots': unique_slots,
        'days': days,
        'grouped_data': grouped_data,
        'selected_department': selected_department,
        'selected_semester': selected_semester,
    })


# =========================
# DEPARTMENT
# =========================

@login_required
def add_department(request):

    show_list = request.GET.get("view_list") == "true"

    if request.method == "POST":

        name = request.POST.get("name", "").strip()

        if name:

            # SAVE DEPARTMENT

            department = Department.objects.create(
                name=name
            )

            # RECENT ACTIVITY

            RecentActivity.objects.create(
                title=f"Added new department {department.name}",
                action_type='Department'
            )

            return redirect(
                reverse('add_department') + '?view_list=true'
            )

    return render(request, "add_department.html", {
        "departments": Department.objects.all(),
        "semesters": Semester.objects.all(),
        "faculties": Faculty.objects.all(),
        "subjects": Subject.objects.all(),
        "dept_list": Department.objects.all() if show_list else None,
        "show_list": show_list,
    })


@login_required
def delete_department(request, id):

    department = get_object_or_404(
        Department,
        id=id
    )

    # RECENT ACTIVITY

    RecentActivity.objects.create(
        title=f"Removed department {department.name}",
        action_type='Department'
    )

    department.delete()

    return redirect(
        reverse('add_department') + '?view_list=true'
    )


# =========================
# SEMESTER
# =========================

@login_required
def add_semester(request):

    show_list = request.GET.get("view_list") == "true"

    form = SemesterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        # SAVE SEMESTER

        semester = form.save()

        # RECENT ACTIVITY

        RecentActivity.objects.create(
            title=f"Added new semester {semester}",
            action_type='Semester'
        )

        return redirect(
            reverse('add_semester') + '?view_list=true'
        )

    return render(request, 'add_semester.html', {
        'form': form,
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
        'faculties': Faculty.objects.all(),
        'subjects': Subject.objects.all(),
        'semester_list': Semester.objects.all() if show_list else None,
        'show_list': show_list,
    })


@login_required
def delete_semester(request, id):

    semester = get_object_or_404(
        Semester,
        id=id
    )

    # RECENT ACTIVITY

    RecentActivity.objects.create(
        title=f"Removed semester {semester}",
        action_type='Semester'
    )

    semester.delete()

    return redirect(
        reverse('add_semester') + '?view_list=true'
    )


# =========================
# FACULTY
# =========================

@login_required
def add_faculty(request):

    show_list = request.GET.get("view_list") == "true"

    form = FacultyForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        # SAVE FACULTY

        faculty = form.save()

        # RECENT ACTIVITY

        RecentActivity.objects.create(
            title=f"Added new faculty {faculty.name}",
            action_type='Faculty'
        )

        return redirect(
            reverse('add_faculty') + '?view_list=true'
        )

    return render(request, 'add_faculty.html', {
        'form': form,
        'title': 'Add Faculty',
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
        'subjects': Subject.objects.all(),
        'faculties_count': Faculty.objects.count(),
        'faculties': Faculty.objects.all() if show_list else None,
    })


@login_required
def delete_faculty(request, id):

    faculty = get_object_or_404(
        Faculty,
        id=id
    )

    # RECENT ACTIVITY

    RecentActivity.objects.create(
        title=f"Removed faculty {faculty.name}",
        action_type='Faculty'
    )

    faculty.delete()

    return redirect(
        reverse('add_faculty') + '?view_list=true'
    )


# =========================
# SUBJECT
# =========================

@login_required
def add_subject(request):

    show_list = request.GET.get("view_list") == "true"

    form = SubjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        # SAVE SUBJECT

        subject = form.save()

        # RECENT ACTIVITY

        RecentActivity.objects.create(
            title=f"Added new subject {subject.name}",
            action_type='Subject'
        )

        return redirect(
            reverse('add_subject') + '?view_list=true'
        )

    return render(request, 'add_subject.html', {
        'form': form,
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
        'faculties': Faculty.objects.all(),
        'subjects': Subject.objects.all(),
        'subject_list': Subject.objects.all() if show_list else None,
        'show_list': show_list,
    })


@login_required
def delete_subject(request, id):

    subject = get_object_or_404(
        Subject,
        id=id
    )

    # RECENT ACTIVITY

    RecentActivity.objects.create(
        title=f"Removed subject {subject.name}",
        action_type='Subject'
    )

    subject.delete()

    return redirect(
        reverse('add_subject') + '?view_list=true'
    )


# =========================
# SUBJECT–FACULTY ASSIGNMENT
# =========================

@login_required
def add_subject_faculty(request):

    show_list = request.GET.get("view_list") == "true"

    if request.method == 'POST':

        subject_id = request.POST.get('subject')
        faculty_id = request.POST.get('faculty')

        if subject_id and faculty_id:

            assignment, created = SubjectFaculty.objects.get_or_create(
                subject_id=subject_id,
                faculty_id=faculty_id
            )

            # RECENT ACTIVITY

            if created:

                RecentActivity.objects.create(
                    title=f"Assigned {assignment.subject.name} to {assignment.faculty.name}",
                    action_type='Subject Faculty'
                )

        return redirect(
            reverse('add_subject_faculty') + '?view_list=true'
        )

    return render(request, 'add_subject_faculty.html', {
        'subjects': Subject.objects.all(),
        'faculties': Faculty.objects.all(),
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
        'assignment_list': SubjectFaculty.objects.all() if show_list else None,
        'show_list': show_list,
    })


@login_required
def delete_subject_faculty(request, id):

    assignment = get_object_or_404(
        SubjectFaculty,
        id=id
    )

    # RECENT ACTIVITY

    RecentActivity.objects.create(
        title=f"Removed subject assignment {assignment.subject.name} from {assignment.faculty.name}",
        action_type='Subject Faculty'
    )

    assignment.delete()

    return redirect(
        reverse('add_subject_faculty') + '?view_list=true'
    )


# =========================
# CLASSROOM
# =========================

@login_required
def add_classroom(request):

    show_list = request.GET.get("view_list") == "true"

    form = ClassroomForm(request.POST or None)

    if request.method == "POST" and form.is_valid():

        # SAVE CLASSROOM

        classroom = form.save()

        # RECENT ACTIVITY

        RecentActivity.objects.create(
            title=f"Added new classroom {classroom.room_number}",
            action_type='Classroom'
        )

        return redirect(
            reverse('add_classroom') + '?view_list=true'
        )

    return render(request, 'add_classroom.html', {
        'form': form,
        'departments': Department.objects.all(),
        'semesters': Semester.objects.all(),
        'faculties': Faculty.objects.all(),
        'classrooms': Classroom.objects.all(),
        'show_list': show_list,
    })


@login_required
def delete_classroom(request, id):

    classroom = get_object_or_404(
        Classroom,
        id=id
    )

    # RECENT ACTIVITY

    RecentActivity.objects.create(
        title=f"Removed classroom {classroom.room_number}",
        action_type='Classroom'
    )

    classroom.delete()

    return redirect(
        reverse('add_classroom') + '?view_list=true'
    )


# =========================
# TIMESLOT
# =========================

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import (
    Department,
    Semester,
    Faculty,
    Subject,
    TimeSlot,
    RecentActivity
)

from .forms import TimeSlotForm


# ==================================================
# ADD TIMESLOT
# ==================================================

@login_required
def add_timeslot(request):

    # show list
    show_list = request.GET.get("view_list") == "true"

    # form
    form = TimeSlotForm(request.POST or None)

    # SAVE
    if request.method == "POST":

        if form.is_valid():

            # SAVE TIMESLOT

            timeslot = form.save()

            # RECENT ACTIVITY

            RecentActivity.objects.create(
                title=f"Added new timeslot {timeslot}",
                action_type='Timing'
            )

            return redirect(
                reverse('add_timeslot') + '?view_list=true'
            )

    context = {

        'form': form,

        'title': 'Add Time Slot',

        # stats
        'departments': Department.objects.count(),
        'semesters': Semester.objects.count(),
        'faculties': Faculty.objects.count(),
        'subjects': Subject.objects.count(),

        # list
        'timeslots': TimeSlot.objects.all()
        if show_list else None,

        'show_list': show_list,
    }

    return render(
        request,
        'add_timeslot.html',
        context
    )


# ==================================================
# DELETE TIMESLOT
# ==================================================

@login_required
def delete_timeslot(request, id):

    timeslot = get_object_or_404(
        TimeSlot,
        id=id
    )

    # RECENT ACTIVITY

    RecentActivity.objects.create(
        title=f"Removed timeslot {timeslot}",
        action_type='Timing'
    )

    timeslot.delete()

    return redirect(
        reverse('add_timeslot') + '?view_list=true'
    )

    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Timetable


#   =========================
#   Generate TIMETABLE (Admin)
#   =========================
@login_required
def timetable(request):

    timetables = Timetable.objects.all()

    return render(
        request,
        'timetable.html',
        {
            'timetables': timetables
        }
    )
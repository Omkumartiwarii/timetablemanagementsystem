from django.shortcuts import render, redirect
from django.http import request
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import *
from .models import *
from .render import Render
import random as rnd

# -----------------------
# Genetic Algorithm Constants
# -----------------------
POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05

# -----------------------
# Data Class
# -----------------------
class Data:
    def __init__(self):
        self._rooms = Room.objects.all()
        self._meetingTimes = MeetingTime.objects.all()
        self._instructors = Instructor.objects.all()
        self._courses = Course.objects.all()
        self._depts = Department.objects.all()

    def get_rooms(self): return self._rooms
    def get_instructors(self): return self._instructors
    def get_courses(self): return self._courses
    def get_depts(self): return self._depts
    def get_meetingTimes(self): return self._meetingTimes

# -----------------------
# Class Model for Schedule
# -----------------------
class Class:
    def __init__(self, id, dept, section, course):
        self.section_id = id
        self.department = dept
        self.course = course
        self.instructor = None
        self.meeting_time = None
        self.room = None
        self.section = section  # store the Section object, not section_id

    def get_id(self): return self.section_id
    def get_dept(self): return self.department
    def get_course(self): return self.course
    def get_instructor(self): return self.instructor
    def get_meetingTime(self): return self.meeting_time
    def get_room(self): return self.room
    def set_instructor(self, instructor): self.instructor = instructor
    def set_meetingTime(self, meetingTime): self.meeting_time = meetingTime
    def set_room(self, room): self.room = room

# -----------------------
# Schedule Class
# -----------------------
class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def initialize(self):
        sections = Section.objects.all()
        for section in sections:
            dept = section.department
            n = section.num_class_in_week
            total_times = len(MeetingTime.objects.all())
            courses = dept.courses.all()

            for course in courses:
                for i in range(min(n // len(courses), total_times)):
                    crs_inst = course.instructors.all()
                    if not crs_inst:
                        print(f"WARNING: No instructors assigned to course {course.course_name} ({course.course_number}), skipping.")
                        continue
                    newClass = Class(self._classNumb, dept, section.section_id, course)
                    self._classNumb += 1
                    newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, total_times)])
                    newClass.set_room(data.get_rooms()[rnd.randrange(0, len(data.get_rooms()))])
                    newClass.set_instructor(crs_inst[rnd.randrange(0, len(crs_inst))])
                    self._classes.append(newClass)
        return self

    def get_classes(self): return self._classes

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            if classes[i].room.seating_capacity < int(classes[i].course.max_numb_students):
                self._numberOfConflicts += 1
            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].meeting_time == classes[j].meeting_time) and \
                       (classes[i].section_id != classes[j].section_id) and \
                       (classes[i].section == classes[j].section):
                        if classes[i].room == classes[j].room:
                            self._numberOfConflicts += 1
                        if classes[i].instructor == classes[j].instructor:
                            self._numberOfConflicts += 1
        return 1 / (1.0 * self._numberOfConflicts + 1)

# -----------------------
# Population Class
# -----------------------
class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = [Schedule().initialize() for i in range(size)]

    def get_schedules(self): return self._schedules

# -----------------------
# Genetic Algorithm Class
# -----------------------
class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        # Preserve elites
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        for _ in range(TOURNAMENT_SELECTION_SIZE):
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop

# -----------------------
# Initialize Data
# -----------------------
data = Data()

# -----------------------
# Context Manager for Template
# -----------------------
def context_manager(schedule):
    classes = schedule.get_classes()
    context = []
    for cls_obj in classes:
        cls = {}
        cls["section"] = cls_obj.section_id
        cls['dept'] = cls_obj.department.dept_name
        cls['course'] = f'{cls_obj.course.course_name} ({cls_obj.course.course_number}, {cls_obj.course.max_numb_students})'
        cls['room'] = f'{cls_obj.room.r_number} ({cls_obj.room.seating_capacity})'
        cls['instructor'] = f'{cls_obj.instructor.name} ({cls_obj.instructor.uid})'
        cls['meeting_time'] = [cls_obj.meeting_time.pid, cls_obj.meeting_time.day, cls_obj.meeting_time.time]
        context.append(cls)
    return context

# -----------------------
# Timetable Generation View
# -----------------------
def timetable(request):
    # Generate the schedule using your GA
    population = Population(POPULATION_SIZE)
    population.get_schedules().sort(key=lambda x: x.calculate_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    
    while population.get_schedules()[0].calculate_fitness() != 1.0:
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.calculate_fitness(), reverse=True)
    
    best_schedule = population.get_schedules()[0].get_classes()

    # Build a list of dicts that template can read
    schedule_data = []
    for cls in best_schedule:
        schedule_data.append({
            "section_id": cls.section.section_id,
            "department": cls.department.dept_name,
            "course_name": cls.course.course_name,
            "course_number": cls.course.course_number,
            "max_students": cls.course.max_numb_students,
            "room_number": cls.room.r_number,
            "room_capacity": cls.room.seating_capacity,
            "instructor_name": cls.instructor.name,
            "instructor_uid": cls.instructor.uid,
            "meeting_day": cls.meeting_time.day,
            "meeting_time": cls.meeting_time.time,
        })

    return render(request, 'gentimetable.html', {
        'schedule': schedule_data,
        'sections': Section.objects.all()
    })

# -----------------------
# Static Pages
# -----------------------
def index(request): return render(request, 'index.html', {})
def about(request): return render(request, 'aboutus.html', {})
def help(request): return render(request, 'help.html', {})
def terms(request): return render(request, 'terms.html', {})

def contact(request):
    if request.method == 'POST':
        message = request.POST['message']
        send_mail('TTGS Contact', message, settings.EMAIL_HOST_USER,
                  ['codevoid12@gmail.com'], fail_silently=False)
    return render(request, 'contact.html', {})

# -----------------------
# Admin Dashboard
# -----------------------
@login_required
def admindash(request):
    return render(request, 'admindashboard.html', {})

# -----------------------
# CRUD Views for Courses
# -----------------------
@login_required
def addCourses(request):
    form = CourseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('addCourses')
    return render(request, 'addCourses.html', {'form': form})

@login_required
def course_list_view(request):
    return render(request, 'courseslist.html', {'courses': Course.objects.all()})

@login_required
def delete_course(request, pk):
    crs = Course.objects.filter(pk=pk)
    if request.method == 'POST':
        crs.delete()
        return redirect('editcourse')

# -----------------------
# CRUD Views for Instructors
# -----------------------
@login_required
def addInstructor(request):
    form = InstructorForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('addInstructors')
    return render(request, 'addInstructors.html', {'form': form})

@login_required
def inst_list_view(request):
    return render(request, 'inslist.html', {'instructors': Instructor.objects.all()})

@login_required
def delete_instructor(request, pk):
    inst = Instructor.objects.filter(pk=pk)
    if request.method == 'POST':
        inst.delete()
        return redirect('editinstructor')

# -----------------------
# CRUD Views for Rooms
# -----------------------
@login_required
def addRooms(request):
    form = RoomForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('addRooms')
    return render(request, 'addRooms.html', {'form': form})

@login_required
def room_list(request):
    return render(request, 'roomslist.html', {'rooms': Room.objects.all()})

@login_required
def delete_room(request, pk):
    rm = Room.objects.filter(pk=pk)
    if request.method == 'POST':
        rm.delete()
        return redirect('editrooms')

# -----------------------
# CRUD Views for Meeting Times
# -----------------------
@login_required
def addTimings(request):
    form = MeetingTimeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('addTimings')
    return render(request, 'addTimings.html', {'form': form})

@login_required
def meeting_list_view(request):
    return render(request, 'mtlist.html', {'meeting_times': MeetingTime.objects.all()})

@login_required
def delete_meeting_time(request, pk):
    mt = MeetingTime.objects.filter(pk=pk)
    if request.method == 'POST':
        mt.delete()
        return redirect('editmeetingtime')

# -----------------------
# CRUD Views for Departments
# -----------------------
@login_required
def addDepts(request):
    form = DepartmentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('addDepts')
    return render(request, 'addDepts.html', {'form': form})

@login_required
def department_list(request):
    return render(request, 'deptlist.html', {'departments': Department.objects.all()})

@login_required
def delete_department(request, pk):
    dept = Department.objects.filter(pk=pk)
    if request.method == 'POST':
        dept.delete()
        return redirect('editdepartment')

# -----------------------
# CRUD Views for Sections
# -----------------------
@login_required
def addSections(request):
    form = SectionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('addSections')
    return render(request, 'addSections.html', {'form': form})

@login_required
def section_list(request):
    return render(request, 'seclist.html', {'sections': Section.objects.all()})

@login_required
def delete_section(request, pk):
    sec = Section.objects.filter(pk=pk)
    if request.method == 'POST':
        sec.delete()
        return redirect('editsection')

# -----------------------
# Timetable Generate Page
# -----------------------
@login_required
def generate(request):
    return render(request, 'generate.html', {})

# -----------------------
# PDF Generation Class
# -----------------------
class Pdf(View):
    def get(self, request):
        params = {'request': request}
        return Render.render('gentimetable.html', params)
    
#chatbot API view

  
from django.http import HttpResponse

def get_bot_response(request):

    user_msg = request.GET.get('msg')

    if user_msg is None:
        return HttpResponse("Please ask something.")

    msg = user_msg.lower()

    if "hello" in msg or "hi" in msg:
        return HttpResponse("Hello 👋 How can I help you with TimeTable Management System?")

    elif "generate" in msg:
        return HttpResponse("Go to Home page and click 'Generate Timetable'.")

    elif "course" in msg:
        return HttpResponse("Go to Admin Dashboard and add Courses first.")

    elif "teacher" in msg:
        return HttpResponse("Go to Add Teachers section to add faculty.")

    elif "room" in msg:
        return HttpResponse("You can add rooms in the Add Rooms section.")

    elif "timetable" in msg:
        return HttpResponse("Click Generate Timetable from the dashboard.")

    else:
        return HttpResponse("Sorry, I didn't understand. Please ask about timetable generation.")
import random
from .models import Subject, SubjectFaculty, Classroom, TimeSlot

POPULATION_SIZE = 8
GENERATIONS = 30
MUTATION_RATE = 0.2


# =========================
# ✅ GLOBAL VALIDATION
# =========================
def is_valid_timetable(timetable):

    used_faculty = set()
    used_rooms = set()
    used_group = set()

    faculty_count = {}
    semester_room_map = {}
    faculty_schedule = {}

    for entry in timetable:

        slot = entry['slot']
        faculty = entry['faculty']
        room = entry['classroom']

        group_id = (
            entry['subject'].semester.department.id,
            entry['subject'].semester.semester_number
        )

        # -------------------
        # Clash checks
        # -------------------
        if (slot.id, faculty.id) in used_faculty:
            return False

        if (slot.id, room.id) in used_rooms:
            return False

        if (slot.id, group_id) in used_group:
            return False

        used_faculty.add((slot.id, faculty.id))
        used_rooms.add((slot.id, room.id))
        used_group.add((slot.id, group_id))

        # -------------------
        # Faculty weekly limit (max 3)
        # -------------------
        faculty_count[faculty.id] = faculty_count.get(faculty.id, 0) + 1
        if faculty_count[faculty.id] > 3:
            return False

        # -------------------
        # Same semester same classroom
        # -------------------
        sem_id = entry['subject'].semester.id

        if sem_id in semester_room_map:
            if semester_room_map[sem_id] != room.id:
                return False
        else:
            semester_room_map[sem_id] = room.id

        # -------------------
        # No continuous classes
        # -------------------
        key = (faculty.id, slot.day)

        if key not in faculty_schedule:
            faculty_schedule[key] = []

        faculty_schedule[key].append(slot.order)

    # Check continuous slots
    for orders in faculty_schedule.values():
        orders.sort()
        for i in range(len(orders) - 1):
            if orders[i+1] - orders[i] == 1:
                return False

    return True


# =========================
# ✅ SAFE ASSIGNMENT
# =========================
def get_safe_assignment(timetable, subject, faculty_list, rooms, slots):

    random.shuffle(slots)
    random.shuffle(rooms)
    random.shuffle(faculty_list)

    group_id = (
        subject.semester.department.id,
        subject.semester.semester_number
    )

    for slot in slots:
        for room in rooms:
            for faculty in faculty_list:

                clash = False

                # Faculty weekly count
                count = sum(1 for e in timetable if e['faculty'] == faculty)
                if count >= 3:
                    continue

                for entry in timetable:

                    if entry['slot'] == slot and entry['faculty'] == faculty:
                        clash = True

                    if entry['slot'] == slot and entry['classroom'] == room:
                        clash = True

                    if (
                        entry['slot'] == slot and
                        (
                            entry['subject'].semester.department.id,
                            entry['subject'].semester.semester_number
                        ) == group_id
                    ):
                        clash = True

                    # No continuous classes
                    if entry['faculty'] == faculty and entry['slot'].day == slot.day:
                        if abs(entry['slot'].order - slot.order) == 1:
                            clash = True

                    if clash:
                        break

                if not clash:
                    return slot, room, faculty

    return None, None, None


# =========================
# ✅ CREATE INDIVIDUAL
# =========================
def create_individual(semester):

    if semester.department.name == "ALL":
        subjects = list(
            Subject.objects.filter(
                semester__semester_number=semester.semester_number
            )
        )
    else:
        subjects = list(Subject.objects.filter(semester=semester))

    rooms = list(Classroom.objects.all())
    slots = list(TimeSlot.objects.all())

    timetable = []
    semester_room_map = {}

    for sub in subjects:

        mappings = SubjectFaculty.objects.filter(subject=sub)
        if not mappings.exists():
            continue

        faculty_list = [m.faculty for m in mappings]
        lectures = getattr(sub, "lectures_per_week", 3)

        # Fixed classroom per semester
        sem_id = sub.semester.id

        if sem_id not in semester_room_map:
            semester_room_map[sem_id] = random.choice(rooms)

        fixed_room = semester_room_map[sem_id]

        for _ in range(lectures):

            slot, room, faculty = get_safe_assignment(
                timetable, sub, faculty_list, [fixed_room], slots
            )

            if slot is None:
                continue

            timetable.append({
                'subject': sub,
                'faculty': faculty,
                'classroom': room,
                'slot': slot
            })

    return timetable


# =========================
# ✅ FITNESS
# =========================
def fitness(timetable, semester):

    score = 0
    subject_day_map = {}

    for entry in timetable:

        subject = entry['subject']
        day = entry['slot'].day

        key = (subject.id, day)

        if key in subject_day_map:
            score -= 5
        else:
            score += 5

        subject_day_map[key] = True

    return score


# =========================
# ✅ SELECTION
# =========================
def selection(population, semester):
    population.sort(key=lambda x: fitness(x, semester), reverse=True)
    return population[:2]


# =========================
# ✅ CROSSOVER
# =========================
def crossover(parent1, parent2, semester):

    child = []
    combined = parent1 + parent2
    random.shuffle(combined)

    for entry in combined:
        temp = child + [entry]
        if is_valid_timetable(temp):
            child.append(entry)

    return child


# =========================
# ✅ MUTATION
# =========================
def mutate(timetable):

    timeslots = list(TimeSlot.objects.all())

    for _ in range(2):

        if not timetable:
            return timetable

        index = random.randint(0, len(timetable) - 1)
        entry = timetable[index]

        for _ in range(10):

            new_slot = random.choice(timeslots)

            clash = False

            for e in timetable:

                if e == entry:
                    continue

                if (
                    e['slot'] == new_slot and
                    (
                        e['faculty'] == entry['faculty'] or
                        e['classroom'] == entry['classroom'] or
                        e['subject'].semester == entry['subject'].semester
                    )
                ):
                    clash = True

                # continuous check
                if e['faculty'] == entry['faculty'] and e['slot'].day == new_slot.day:
                    if abs(e['slot'].order - new_slot.order) == 1:
                        clash = True

                if clash:
                    break

            if not clash:
                entry['slot'] = new_slot
                break

    return timetable


# =========================
# ✅ MAIN FUNCTION
# =========================
def generate_timetable(semester):

    population = []

    while len(population) < POPULATION_SIZE:
        ind = create_individual(semester)
        if is_valid_timetable(ind):
            population.append(ind)

    for generation in range(GENERATIONS):

        parents = selection(population, semester)
        best = parents[0]

        new_population = [best]

        while len(new_population) < POPULATION_SIZE:

            child = crossover(parents[0], parents[1], semester)

            if random.random() < MUTATION_RATE:
                child = mutate(child)

            # ✅ FIXED VALIDATION LOOP
            while not is_valid_timetable(child):
                child = create_individual(semester)

            new_population.append(child)

        population = new_population
        print(f"Generation {generation} done")

    best = max(population, key=lambda x: fitness(x, semester))

    print("FINAL BEST:", best)  # 🔥 DEBUG

    return best
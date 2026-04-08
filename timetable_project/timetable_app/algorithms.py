import random
from .models import Subject, SubjectFaculty, Classroom, TimeSlot


def generate_timetable(semester):
    subjects = list(Subject.objects.filter(semester=semester))
    rooms = list(Classroom.objects.all())
    slots = list(TimeSlot.objects.all())

    if not subjects or not rooms or not slots:
        return []

    # 🔥 Shuffle slots → fixes "only Monday" issue
    random.shuffle(slots)

    timetable = []

    used_faculty = set()
    used_rooms = set()
    used_semester_slots = set()

    for sub in subjects:
        mappings = SubjectFaculty.objects.filter(subject=sub)

        if not mappings.exists():
            continue

        faculty_list = [m.faculty for m in mappings]

        for _ in range(3):

            assigned = False

        # Try multiple combinations before giving up
            for _ in range(50):   # 🔥 retry mechanism

                faculty = random.choice(faculty_list)
                slot = random.choice(slots)
                room = random.choice(rooms)

                # Check clashes
                if (slot.id, faculty.id) in used_faculty:
                    continue

                if (slot.id, room.id) in used_rooms:
                    continue
                if (slot.id, semester.id) in used_semester_slots:
                    continue

                # Assign
                timetable.append({
                    'subject': sub,
                    'faculty': faculty,
                    'classroom': room,
                    'slot': slot,
                    'day': slot.day
                })

                used_faculty.add((slot.id, faculty.id))
                used_rooms.add((slot.id, room.id))
                used_semester_slots.add((slot.id, semester.id))

                assigned = True
                break

            # If still not assigned → force assign (avoid missing subjects)
            if not assigned:
                timetable.append({
                    'subject': sub,
                    'faculty': faculty_list[0],
                    'classroom': rooms[0],
                    'slot': slots[0],
                    'day': slots[0].day
                })

    return timetable
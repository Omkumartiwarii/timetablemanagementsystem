import random

from .models import (
    Subject,
    SubjectFaculty,
    Classroom,
    TimeSlot,
    Timetable
)

MAX_FACULTY_PER_DAY = 4
MAX_RETRIES = 200


# -----------------------------------
# Utility
# -----------------------------------

def all_slots():
    return list(
        TimeSlot.objects.all().order_by(
            "day","order"
        )
    )


def consecutive_pairs():

    pairs=[]

    days=[
        "Monday","Tuesday",
        "Wednesday","Thursday",
        "Friday","Saturday"
    ]

    for d in days:

        ds=list(
            TimeSlot.objects.filter(
                day=d
            ).order_by("order")
        )

        for i in range(
            len(ds)-1
        ):
            if ds[i+1].order == ds[i].order+1:

                pairs.append(
                    (ds[i],ds[i+1])
                )

    return pairs


# -----------------------------------
# HARD CONSTRAINT CHECKS
# -----------------------------------

def faculty_load(schedule,faculty,day):

    return sum(
        1 for e in schedule
        if faculty in e["faculties"]
        and e["slot"].day==day
    )


def faculty_adjacent(schedule,faculty,slot):

    for e in schedule:

        if (
            faculty in e["faculties"]
            and
            e["slot"].day==slot.day
            and abs(
                e["slot"].order -
                slot.order
            )==1
        ):
            return True

    return False


def clash(
    schedule,
    semester,
    slot,
    room,
    faculties
):

    for e in schedule:

        # semester only one class
        if (
            e["semester"].id==semester.id
            and e["slot"]==slot
        ):
            return True

        # room clash
        if (
            e["slot"]==slot
            and e["room"]==room
        ):
            return True

        # faculty clash
        for f in faculties:
            if (
                e["slot"]==slot
                and f in e["faculties"]
            ):
                return True

    return False


# -----------------------------------
# SUBJECT DEMANDS
# -----------------------------------

def build_demands(semester):

    demands=[]

    subs=Subject.objects.filter(
        semester=semester
    )

    for s in subs:

        maps=list(
            SubjectFaculty.objects.filter(
                subject=s
            )
        )

        if not maps:
            continue

        # THEORY
        if not s.is_lab:

            one_faculty=random.choice(
                maps
            ).faculty

            periods=s.credits

            for _ in range(periods):

                demands.append({
                    "type":"theory",
                    "subject":s,
                    "faculties":[one_faculty]
                })


        # LAB
        else:

            if len(maps)<2:
                continue

            if s.credits==2:
                sessions=1
            elif s.credits==3:
                sessions=2
            else:
                sessions=1

            for _ in range(sessions):

                demands.append({
                    "type":"lab",
                    "subject":s,
                    "faculties":[
                        maps[0].faculty,
                        maps[1].faculty
                    ]
                })

    # labs first
    demands.sort(
        key=lambda x:
        0 if x["type"]=="lab"
        else 1
    )

    return demands


# -----------------------------------
# TRY BUILD FULL SCHEDULE
# -----------------------------------

def try_construct(semester):

    theory_rooms=list(
        Classroom.objects.filter(
            is_lab=False
        )
    )

    lab_rooms=list(
        Classroom.objects.filter(
            is_lab=True
        )
    )

    if not theory_rooms:
        return None

    fixed_room=random.choice(
        theory_rooms
    )

    schedule=[]

    demands=build_demands(
        semester
    )

    for d in demands:

        placed=False

        # -----------------
        # LAB
        # -----------------

        if d["type"]=="lab":

            pairs=consecutive_pairs()
            random.shuffle(pairs)

            for s1,s2 in pairs:

                room=random.choice(
                    lab_rooms
                )

                bad=False

                for f in d["faculties"]:

                    if (
                       faculty_load(
                          schedule,
                          f,
                          s1.day
                       )
                       >=
                       MAX_FACULTY_PER_DAY
                    ):
                        bad=True

                if bad:
                    continue

                if clash(
                    schedule,
                    semester,
                    s1,
                    room,
                    d["faculties"]
                ):
                    continue

                if clash(
                    schedule,
                    semester,
                    s2,
                    room,
                    d["faculties"]
                ):
                    continue


                schedule.append({
                    "semester":semester,
                    "subject":d["subject"],
                    "faculties":d["faculties"],
                    "room":room,
                    "slot":s1
                })

                schedule.append({
                    "semester":semester,
                    "subject":d["subject"],
                    "faculties":d["faculties"],
                    "room":room,
                    "slot":s2
                })

                placed=True
                break


        # -----------------
        # THEORY
        # -----------------

        else:

            slots=all_slots()
            random.shuffle(slots)

            f=d["faculties"][0]

            for slot in slots:

                if faculty_load(
                    schedule,
                    f,
                    slot.day
                )>=MAX_FACULTY_PER_DAY:
                    continue

                if faculty_adjacent(
                    schedule,
                    f,
                    slot
                ):
                    continue

                if clash(
                    schedule,
                    semester,
                    slot,
                    fixed_room,
                    [f]
                ):
                    continue


                schedule.append({
                    "semester":semester,
                    "subject":d["subject"],
                    "faculties":[f],
                    "room":fixed_room,
                    "slot":slot
                })

                placed=True
                break


        # if any demand unscheduled -> fail
        if not placed:
            return None

    return schedule


# -----------------------------------
# MAIN GENERATOR
# -----------------------------------

def generate_timetable(
    semester
):

    Timetable.objects.filter(
        semester=semester
    ).delete()

    final_schedule=None

    # retry until feasible
    for _ in range(
        MAX_RETRIES
    ):

        s=try_construct(
            semester
        )

        if s:
            final_schedule=s
            break


    if not final_schedule:
        raise Exception(
          f"No feasible timetable for {semester}"
        )


    # save
    for e in final_schedule:

        row=Timetable.objects.create(
            semester=e["semester"],
            subject=e["subject"],
            classroom=e["room"],
            timeslot=e["slot"]
        )

        row.faculty.set(
            e["faculties"]
        )

    return final_schedule

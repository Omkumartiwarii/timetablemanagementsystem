import random

from .models import (
    Subject,
    SubjectFaculty,
    Classroom,
    TimeSlot,
    Timetable,
    SubjectLabRoom
)

MAX_FACULTY_PER_DAY = 4
MAX_RETRIES = 200

# ─────────────────────────────────────────────
# SHIFT DETECTION
# ─────────────────────────────────────────────

def get_slot_shift(slot):
    """
    Returns "first" or "second" based on whether the slot
    falls before or after 13:00 (1 PM).

    Relies on TimeSlot.start_time (a datetime.time field).
    If your model uses a string, adjust the comparison below.
    """
    import datetime
    cutoff = datetime.time(13, 0)          # 1:00 PM

    try:
        t = slot.start_time                # preferred: actual time field
        if isinstance(t, str):
            # fallback: parse "HH:MM" or "HH:MM:SS"
            t = datetime.time(*map(int, t.split(":")[:2]))
        return "first" if t < cutoff else "second"
    except Exception:
        # last resort: use slot order heuristic (≤4 → first shift)
        return "first" if slot.order <= 4 else "second"


# ─────────────────────────────────────────────
# CLASSROOM PRE-ASSIGNMENT  (NEW)
# ─────────────────────────────────────────────

def assign_preferred_classrooms(semesters, theory_rooms):
    """
    Returns a dict:  semester_id  →  {"first": room, "second": room}

    Strategy
    ────────
    We have N theory rooms and S semesters.
    Each shift can accommodate N semesters independently (same room
    can be reused across shifts because the time windows don't overlap).

    Round-robin assignment ensures every semester gets a preferred room
    for each shift.  If S > N the same room is shared by multiple
    semesters in the same shift, but the clash() guard will still
    prevent actual double-booking.
    """
    assignment = {}
    n = len(theory_rooms)

    if n == 0:
        return assignment

    for idx, sem in enumerate(semesters):
        # Different offset per shift so we spread load differently
        first_room  = theory_rooms[idx % n]
        second_room = theory_rooms[(idx + n // 2) % n]   # offset by half the pool

        assignment[sem.id] = {
            "first":  first_room,
            "second": second_room,
        }

    return assignment


# ─────────────────────────────────────────────
# PENALTIES
# ─────────────────────────────────────────────

def compute_penalty(schedule):
    penalty = 0
    faculty_day_map = {}

    for e in schedule:
        for f in e["faculties"]:
            key = (f.id, e["slot"].day)
            if key not in faculty_day_map:
                faculty_day_map[key] = {"theory": 0, "lab": 0}
            if e["subject"].is_lab:
                faculty_day_map[key]["lab"] += 1
            else:
                faculty_day_map[key]["theory"] += 1

    for (fid, day), loads in faculty_day_map.items():
        theory = loads["theory"]
        lab    = loads["lab"]

        if theory > 3:
            penalty += (theory - 3) * 5
        if theory > 2 and lab >= 1:
            penalty += 5 * (theory - 2)
        if lab > 1:
            penalty += (lab - 1) * 7

    return penalty


def compute_room_stability_penalty(schedule):
    """
    Extra penalty for room switching within a semester on the same day.
    Lower is better; 0 means the semester uses exactly one room per day.
    Used only for logging / diagnostics — NOT for feasibility decisions.
    """
    sem_day_rooms = {}
    for e in schedule:
        key = (e["semester"].id, e["slot"].day)
        sem_day_rooms.setdefault(key, set()).add(e["room"].id)

    return sum(len(rooms) - 1 for rooms in sem_day_rooms.values())


# ─────────────────────────────────────────────
# UTILITIES
# ─────────────────────────────────────────────

def all_slots():
    return list(
        TimeSlot.objects.filter(is_break=False).order_by("day", "order")
    )


def consecutive_pairs():
    pairs = []
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    for d in days:
        ds = list(
            TimeSlot.objects.filter(day=d, is_break=False).order_by("order")
        )
        for i in range(len(ds) - 1):
            s1, s2 = ds[i], ds[i + 1]
            if valid_lab_pair(s1, s2):
                pairs.append((s1, s2))

    return pairs


def valid_lab_pair(s1, s2):
    if s1.day != s2.day:
        return False
    if s1.is_break or s2.is_break:
        return False
    if s2.order != s1.order + 1:
        return False
    if s1.shift != s2.shift:
        return False
    return True


# ─────────────────────────────────────────────
# HARD CONSTRAINT CHECKS  (unchanged)
# ─────────────────────────────────────────────

def faculty_load(schedule, faculty, day):
    return sum(
        1 for e in schedule
        if faculty in e["faculties"] and e["slot"].day == day
    )


def faculty_adjacent(schedule, faculty, slot):
    for e in schedule:
        if (
            faculty in e["faculties"]
            and e["slot"].day == slot.day
            and abs(e["slot"].order - slot.order) == 1
        ):
            return True
    return False


def clash(schedule, semester, slot, room, faculties):
    for e in schedule:
        if e["semester"].id == semester.id and e["slot"] == slot:
            return True
        if e["slot"] == slot and e["room"] == room:
            return True
        for f in faculties:
            if e["slot"] == slot and f in e["faculties"]:
                return True

    if Timetable.objects.filter(timeslot=slot, classroom=room).exists():
        return True
    for f in faculties:
        if Timetable.objects.filter(timeslot=slot, faculty=f).exists():
            return True

    return False


# ─────────────────────────────────────────────
# SUBJECT DEMANDS  (unchanged)
# ─────────────────────────────────────────────

def build_demands(semester):
    demands = []
    subs = Subject.objects.filter(semester=semester)

    for s in subs:
        maps = list(SubjectFaculty.objects.filter(subject=s))
        if not maps:
            continue

        if not s.is_lab:
            one_faculty = random.choice(maps).faculty
            for _ in range(s.credits):
                demands.append({
                    "type": "theory",
                    "subject": s,
                    "faculties": [one_faculty],
                })
        else:
            if len(maps) < 2:
                continue
            sessions = 2 if s.credits == 3 else 1
            for _ in range(sessions):
                demands.append({
                    "type": "lab",
                    "subject": s,
                    "faculties": [maps[0].faculty, maps[1].faculty],
                })

    demands.sort(key=lambda x: 0 if x["type"] == "lab" else 1)
    return demands


# ─────────────────────────────────────────────
# ORDERED ROOM LIST  (NEW helper)
# ─────────────────────────────────────────────

def ordered_rooms_for_slot(slot, preferred_room, all_theory_rooms):
    """
    Returns a list of theory rooms with `preferred_room` at the front.
    Falls back to the full list if the preferred room is not available
    (clash() will gate actual booking).
    """
    others = [r for r in all_theory_rooms if r.id != preferred_room.id]
    random.shuffle(others)
    return [preferred_room] + others


# ─────────────────────────────────────────────
# TRY BUILD FULL SCHEDULE  (updated)
# ─────────────────────────────────────────────

def try_construct(semester, preferred_rooms, theory_rooms):
    """
    preferred_rooms : {"first": Classroom, "second": Classroom}
                      — the pre-assigned rooms for this semester per shift.
    theory_rooms    : full list of Classroom objects (is_lab=False)
    """
    if not theory_rooms:
        return None

    schedule = []
    demands  = build_demands(semester)
    random.shuffle(demands)

    for d in demands:
        placed = False

        # ── LAB ──────────────────────────────────────────────────────────
        if d["type"] == "lab":
            pairs = consecutive_pairs()
            random.shuffle(pairs)

            mapped_rooms = list(
                SubjectLabRoom.objects.filter(
                    subject=d["subject"]
                ).values_list("classroom", flat=True)
            )
            allowed_rooms = list(Classroom.objects.filter(id__in=mapped_rooms))

            if not allowed_rooms:
                continue

            random.shuffle(allowed_rooms)

            for s1, s2 in pairs:
                for room in allowed_rooms:
                    if clash(schedule, semester, s1, room, d["faculties"]):
                        continue
                    if clash(schedule, semester, s2, room, d["faculties"]):
                        continue

                    schedule.append({
                        "semester": semester,
                        "subject":  d["subject"],
                        "faculties": d["faculties"],
                        "room":  room,
                        "slot":  s1,
                    })
                    schedule.append({
                        "semester": semester,
                        "subject":  d["subject"],
                        "faculties": d["faculties"],
                        "room":  room,
                        "slot":  s2,
                    })
                    placed = True
                    break
                if placed:
                    break

        # ── THEORY ───────────────────────────────────────────────────────
        else:
            slots = all_slots()
            random.shuffle(slots)
            f = d["faculties"][0]

            for slot in slots:
                if faculty_adjacent(schedule, f, slot):
                    continue

                # ── ROOM PREFERENCE (new) ─────────────────────────────
                shift = get_slot_shift(slot)
                pref  = preferred_rooms.get(shift)          # may be None

                if pref:
                    room_order = ordered_rooms_for_slot(
                        slot, pref, theory_rooms
                    )
                else:
                    room_order = list(theory_rooms)
                    random.shuffle(room_order)
                # ─────────────────────────────────────────────────────

                for room in room_order:
                    if clash(schedule, semester, slot, room, [f]):
                        continue

                    schedule.append({
                        "semester": semester,
                        "subject":  d["subject"],
                        "faculties": [f],
                        "room":  room,
                        "slot":  slot,
                    })
                    placed = True
                    break

                if placed:
                    break

        if not placed:
            return None

    return schedule


# ─────────────────────────────────────────────
# MAIN GENERATOR  (updated signature)
# ─────────────────────────────────────────────

def generate_timetable(semester, preferred_rooms, theory_rooms):
    """
    preferred_rooms : {"first": Classroom, "second": Classroom}
    theory_rooms    : pre-fetched list of all non-lab classrooms
    """
    best_schedule = None
    best_penalty  = float("inf")

    for _ in range(MAX_RETRIES):
        s = try_construct(semester, preferred_rooms, theory_rooms)
        if not s:
            continue

        p = compute_penalty(s)
        if p < best_penalty:
            best_penalty  = p
            best_schedule = s

        if p == 0:
            break

    if not best_schedule:
        raise Exception(f"No feasible timetable for {semester}")

    for e in best_schedule:
        row = Timetable.objects.create(
            semester=e["semester"],
            subject=e["subject"],
            classroom=e["room"],
            timeslot=e["slot"],
        )
        row.faculty.set(e["faculties"])

    print(f"[{semester}] Final Penalty: {best_penalty}")
    return best_schedule


# ─────────────────────────────────────────────
# GLOBAL ENTRY POINT  (updated)
# ─────────────────────────────────────────────

def generate_all_timetables(semesters):
    # 1. Wipe old data
    Timetable.objects.all().delete()

    # 2. Fetch resources once
    theory_rooms = list(Classroom.objects.filter(is_lab=False))

    # 3. Pre-assign preferred classrooms (shift-aware)
    preferred_map = assign_preferred_classrooms(semesters, theory_rooms)
    print_preferred_assignment(semesters, preferred_map)

    # 4. Generate per semester
    all_schedules = []
    for sem in semesters:
        pref = preferred_map.get(sem.id, {})
        s    = generate_timetable(sem, pref, theory_rooms)
        all_schedules.extend(s)

    # 5. Diagnostics
    print_global_faculty_daily_load_from_schedule(all_schedules)
    print_room_stability_report(all_schedules)


# ─────────────────────────────────────────────
# DIAGNOSTICS / REPORTING  (new + existing)
# ─────────────────────────────────────────────

def print_preferred_assignment(semesters, preferred_map):
    print("\n📋 PREFERRED CLASSROOM ASSIGNMENTS\n")
    for sem in semesters:
        pref = preferred_map.get(sem.id, {})
        first  = pref.get("first",  "—")
        second = pref.get("second", "—")
        print(f"  {sem}  →  First shift: {first}  |  Second shift: {second}")


def print_room_stability_report(schedule):
    """
    Shows how many distinct rooms each semester used per day.
    A score of 1 means perfect stability (same room all day).
    """
    sem_day_rooms = {}
    for e in schedule:
        key = (e["semester"], e["slot"].day)
        sem_day_rooms.setdefault(key, set()).add(e["room"].id)

    total_switches = 0
    print("\n🏫 ROOM STABILITY REPORT\n")

    for (sem, day), rooms in sorted(
        sem_day_rooms.items(), key=lambda x: (str(x[0][0]), x[0][1])
    ):
        n = len(rooms)
        flag = "✅" if n == 1 else f"🔄 ({n} rooms)"
        print(f"  {sem} | {day}  →  {flag}")
        total_switches += n - 1

    print(f"\n  Total unnecessary room switches: {total_switches}")


def print_global_faculty_daily_load_from_schedule(schedule):
    faculty_day_map = {}

    for e in schedule:
        day = e["slot"].day
        for f in e["faculties"]:
            key = (f.id, f.name, day)
            if key not in faculty_day_map:
                faculty_day_map[key] = {"theory": 0, "lab": 0}
            if e["subject"].is_lab:
                faculty_day_map[key]["lab"] += 1
            else:
                faculty_day_map[key]["theory"] += 1

    print("\n🌍 FINAL GLOBAL FACULTY LOAD\n")
    for (fid, fname, day), load in sorted(faculty_day_map.items()):
        theory  = load["theory"]
        lab     = load["lab"]
        warning = ""
        if theory > 3:
            warning += " ⚠️ >3 Theory"
        if theory > 2 and lab >= 1:
            warning += " ⚠️ 2T+1L violated"
        if lab > 1:
            warning += " ⚠️ >1 Lab"
        print(f"  {fname} | {day} → Theory: {theory}, Lab: {lab}{warning}")
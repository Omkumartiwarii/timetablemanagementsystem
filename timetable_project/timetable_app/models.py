from django.db import models

# =========================
# Department
# =========================
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# Semester
# =========================
class Semester(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester_number = models.IntegerField()

    def __str__(self):
        return f"{self.department.name} - Sem {self.semester_number}"


# =========================
# Faculty (FINAL - only one)
# =========================
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# =========================
# Subject
# =========================
class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# =========================
# Subject-Faculty Mapping
# =========================
class SubjectFaculty(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name} - {self.faculty.name}"


# =========================
# Classroom
# =========================
class Classroom(models.Model):
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Room {self.room_number}"


# =========================
# TimeSlot
# =========================
class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    order = models.IntegerField(default=1)  # For ordering time slots within a day

    def __str__(self):
        return f"{self.day} ({self.start_time} - {self.end_time})"


# =========================
# Timetable
# =========================
class Timetable(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name} | {self.timeslot.day} | {self.timeslot.start_time}"
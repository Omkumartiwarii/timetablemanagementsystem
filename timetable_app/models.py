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
    email = models.EmailField(blank=True,null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# =========================
# Subject
# =========================
class Subject(models.Model):
    name = models.CharField(max_length=100)

    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE
    )

    credits = models.IntegerField(
        default=3
    )

    lectures_per_week = models.IntegerField(
        blank=True,
        null=True
    )

    is_lab = models.BooleanField(
        default=False
    )

    weekly_lab_sessions = models.IntegerField(
        blank=True,
        null=True
    )

    lab_duration = models.IntegerField(
        default=2
    )

    def save(self,*args,**kwargs):

        # theory from credits
        if not self.is_lab:
            self.lectures_per_week = self.credits

        # lab from credits
        else:
            if self.credits == 2:
                self.weekly_lab_sessions = 1

            elif self.credits == 3:
                self.weekly_lab_sessions = 2

        super().save(*args,**kwargs)

    def __str__(self):
        lab_tag = " [Lab]" if self.is_lab else ""
        return f"{self.id} | {self.name} | {self.semester.department.name} Sem {self.semester.semester_number}{lab_tag}"


# =========================
# Subject-Faculty Mapping
# =========================
from django.core.exceptions import ValidationError
class SubjectFaculty(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def clean(self):
        if self.subject.is_lab:
            count=SubjectFaculty.objects.filter(
                subject=self.subject
            ).count()

            if count>=2 and not self.pk:
                raise ValidationError(
                   'Only two faculty allowed for lab.'
                )

    def __str__(self):
        return f"{self.subject.name} - {self.faculty.name}"


# =========================
# Classroom
# =========================
class Classroom(models.Model):

    room_number = models.CharField(
        max_length=100
    )

    capacity = models.IntegerField(default=60)

    is_lab = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.room_number

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
    faculty = models.ManyToManyField(Faculty)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name} | {self.timeslot.day} | {self.timeslot.start_time}"

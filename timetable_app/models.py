from django.db import models
from django.core.exceptions import ValidationError

# =========================
# DUAL DATABASE BASE MODEL
# =========================

class DualDatabaseModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        using = kwargs.pop('using', None)

        # Agar manually DB specify kiya gaya ho
        if using:
            return super().save(using=using, *args, **kwargs)

        # -------------------------
        # SQLITE SAVE
        # -------------------------
        super().save(using='default', *args, **kwargs)

        # Current PK preserve
        sqlite_pk = self.pk

        # -------------------------
        # POSTGRESQL SAVE
        # -------------------------
        try:
            existing = self.__class__.objects.using('postgresql').filter(
                id=sqlite_pk
            ).first()

            if existing:
                # UPDATE EXISTING
                self.pk = sqlite_pk
                super().save(using='postgresql', *args, **kwargs)

            else:
                # CREATE NEW
                self.pk = sqlite_pk
                super().save(using='postgresql', force_insert=True, *args, **kwargs)

        except Exception as e:
            print("PostgreSQL Save Error:", e)

        # restore pk
        self.pk = sqlite_pk

    def delete(self, *args, **kwargs):

        using = kwargs.pop('using', None)

        if using:
            return super().delete(using=using, *args, **kwargs)

        current_pk = self.pk

        # SQLITE DELETE
        try:
            self.__class__.objects.using('default').filter(
                pk=current_pk
            ).delete()
        except Exception as e:
            print("SQLite Delete Error:", e)

        # POSTGRESQL DELETE
        try:
            self.__class__.objects.using('postgresql').filter(
                pk=current_pk
            ).delete()
        except Exception as e:
            print("PostgreSQL Delete Error:", e)


# =========================
# RECENT ACTIVITY
# =========================

class RecentActivity(DualDatabaseModel):

    ACTION_TYPES = (
        ('Department', 'Department'),
        ('Semester', 'Semester'),
        ('Faculty', 'Faculty'),
        ('Subject', 'Subject'),
        ('Subject Faculty', 'Subject Faculty'),
        ('Classroom', 'Classroom'),
        ('Timing', 'Timing'),
        ('Generate', 'Generate'),
        ('Remove', 'Remove'),
        ('Delete', 'Delete'),
        ('Edit', 'Edit'),
        ('Add', 'Add'),
    )

    title = models.CharField(max_length=255)

    action_type = models.CharField(
        max_length=100,
        choices=ACTION_TYPES,
        default='Add'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.action_type} - {self.title}"


# =========================
# Department
# =========================

class Department(DualDatabaseModel):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# =========================
# Semester
# =========================

class Semester(DualDatabaseModel):

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    semester_number = models.IntegerField()

    def __str__(self):
        return f"{self.department.name} - Sem {self.semester_number}"


# =========================
# Faculty
# =========================

class Faculty(DualDatabaseModel):

    name = models.CharField(max_length=100)

    email = models.EmailField(
        blank=True,
        null=True
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


# =========================
# Subject
# =========================

class Subject(DualDatabaseModel):

    name = models.CharField(max_length=100)

    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE
    )

    credits = models.IntegerField(default=3)

    lectures_per_week = models.IntegerField(
        blank=True,
        null=True
    )

    is_lab = models.BooleanField(default=False)

    weekly_lab_sessions = models.IntegerField(
        blank=True,
        null=True
    )

    lab_duration = models.IntegerField(default=2)

    def save(self, *args, **kwargs):

        # THEORY
        if not self.is_lab:
            self.lectures_per_week = self.credits

        # LAB
        else:

            if self.credits == 2:
                self.weekly_lab_sessions = 1

            elif self.credits == 3:
                self.weekly_lab_sessions = 2

        super().save(*args, **kwargs)

    def __str__(self):

        lab_tag = " [Lab]" if self.is_lab else ""

        return (
            f"{self.id} | "
            f"{self.name} | "
            f"{self.semester.department.name} "
            f"Sem {self.semester.semester_number}"
            f"{lab_tag}"
        )


# =========================
# Subject Faculty Mapping
# =========================

class SubjectFaculty(DualDatabaseModel):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.CASCADE
    )

    def clean(self):

        if not self.subject_id:
            return

        if self.subject.is_lab:

            count = SubjectFaculty.objects.filter(
                subject=self.subject
            ).count()

            if count >= 2 and not self.pk:

                raise ValidationError(
                    'Only two faculty allowed for lab.'
                )

    def __str__(self):
        return f"{self.subject.name} - {self.faculty.name}"


# =========================
# Classroom
# =========================

class Classroom(DualDatabaseModel):

    room_number = models.CharField(max_length=100)

    capacity = models.IntegerField(default=60)

    is_lab = models.BooleanField(default=False)

    def __str__(self):
        return self.room_number


# =========================
# TimeSlot
# =========================

class TimeSlot(DualDatabaseModel):

    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    day = models.CharField(
        max_length=10,
        choices=DAY_CHOICES
    )

    start_time = models.TimeField()

    end_time = models.TimeField()

    shift = models.CharField(
        max_length=20,
        choices=[
            ("morning", "Morning"),
            ("afternoon", "Afternoon")
        ]
    )

    order = models.IntegerField(default=1)

    is_break = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.day} ({self.start_time} - {self.end_time})"


# =========================
# Timetable
# =========================

class Timetable(DualDatabaseModel):

    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    faculty = models.ManyToManyField(Faculty)

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE
    )

    timeslot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE
    )

    def __str__(self):

        return (
            f"{self.subject.name} | "
            f"{self.timeslot.day} | "
            f"{self.timeslot.start_time}"
        )


# =========================
# Subject Lab Room
# =========================

class SubjectLabRoom(DualDatabaseModel):

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):

        subject_name = (
            self.subject.name
            if self.subject
            else "No Subject"
        )

        room_name = (
            self.classroom.room_number
            if self.classroom
            else "No Room"
        )

        return f"{subject_name} -> {room_name}"
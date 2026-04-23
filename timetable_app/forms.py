from django import forms
from .models import (
    Department,
    Semester,
    Faculty,
    Subject,
    SubjectFaculty,
    Classroom,
    TimeSlot
)

# =========================
# Department Form
# =========================
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']


# =========================
# Semester Form
# =========================
class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['department', 'semester_number']


# =========================
# Faculty Form
# =========================
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'department']


# =========================
# Subject Form
# =========================
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'semester']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👇 dropdown sorted + clean dikhne ke liye
        self.fields['semester'].queryset = Semester.objects.all().order_by('id')

        # 👇 optional UI improvement
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter Subject Name'
        })


# =========================
# Subject-Faculty Form
# =========================
class SubjectFacultyForm(forms.ModelForm):
    class Meta:
        model = SubjectFaculty
        fields = ['subject', 'faculty']


# =========================
# Classroom Form
# =========================
class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['room_number', 'capacity']


# =========================
# TimeSlot Form
# =========================
class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ['day', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
   
# =========================
# Add Faculty Form
# =========================     
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'department']
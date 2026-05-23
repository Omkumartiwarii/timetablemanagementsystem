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
# class FacultyForm(forms.ModelForm):
#     class Meta:
#         model = Faculty
#         fields = ['name', 'email','department']


# =========================
# Subject Form
# =========================
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'semester','credits','is_lab','lab_duration']

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Subject Name'
            }),

            'semester': forms.Select(attrs={
                'class': 'form-control'
            }),

            'credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Credits'
            }),

            'is_lab': forms.CheckboxInput(attrs={
                'class': 'checkbox-input'
            }),

            'lab_duration': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Lab Duration'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 👇 dropdown sorted + clean dikhne ke liye
        self.fields['semester'].queryset = Semester.objects.all().order_by('id')

        # 👇 optional UI improvement
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Enter Subject Name'
        })
        # hidden initially
        self.fields['lab_duration'].required = False


# =========================
# Subject-Faculty Form
# =========================
class SubjectFacultyForm(forms.ModelForm):

    # extra fields
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False
    )

    semester = forms.ModelChoiceField(
        queryset=Semester.objects.none(),
        required=False
    )

    class Meta:
        model = SubjectFaculty

        fields = [
            'department',
            'semester',
            'subject',
            'faculty'
        ]

        widgets = {

            'department': forms.Select(attrs={
                'class': 'form-control'
            }),

            'semester': forms.Select(attrs={
                'class': 'form-control'
            }),

            'subject': forms.Select(attrs={
                'class': 'form-control'
            }),

            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # initially empty
        self.fields['subject'].queryset = Subject.objects.none()

        # all faculty
        self.fields['faculty'].queryset = Faculty.objects.all().order_by('name')

        # department selected
        if 'department' in self.data:

            try:
                department_id = int(
                    self.data.get('department')
                )

                self.fields['semester'].queryset = (
                    Semester.objects.filter(
                        department_id=department_id
                    ).order_by('semester_number')
                )

            except:
                pass

        # semester selected
        if 'semester' in self.data:

            try:
                semester_id = int(
                    self.data.get('semester')
                )

                self.fields['subject'].queryset = (
                    Subject.objects.filter(
                        semester_id=semester_id
                    ).order_by('name')
                )

            except:
                pass

        # edit mode
        elif self.instance.pk:

            semester = self.instance.subject.semester

            self.fields['semester'].queryset = (
                Semester.objects.filter(
                    department=semester.department
                )
            )

            self.fields['subject'].queryset = (
                Subject.objects.filter(
                    semester=semester
                )
            )

            self.initial['department'] = semester.department
            self.initial['semester'] = semester


# =========================
# Classroom Form
# =========================
class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['room_number', 'is_lab','capacity']


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
        fields = ['name', 'email','department']

# ===========================
# Add subject Lab room
# ===========================
from django import forms

from .models import (
    SubjectLabRoom,
    Subject,
    Classroom,
    Department,
    Semester
)


class SubjectLabRoomForm(forms.ModelForm):

    # FILTER FIELDS
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False
    )

    semester = forms.ModelChoiceField(
        queryset=Semester.objects.none(),
        required=False
    )

    class Meta:

        model = SubjectLabRoom

        fields = [
            'department',
            'semester',
            'subject',
            'classroom'
        ]

        widgets = {

            'department': forms.Select(attrs={
                'class': 'form-control'
            }),

            'semester': forms.Select(attrs={
                'class': 'form-control'
            }),

            'subject': forms.Select(attrs={
                'class': 'form-control'
            }),

            'classroom': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # EMPTY INITIALLY
        self.fields['subject'].queryset = Subject.objects.none()

        # ONLY LAB CLASSROOMS
        self.fields['classroom'].queryset = (
            Classroom.objects.filter(
                is_lab=True
            ).order_by('room_number')
        )

        # DEPARTMENT FILTER
        if 'department' in self.data:

            try:

                department_id = int(
                    self.data.get('department')
                )

                self.fields['semester'].queryset = (
                    Semester.objects.filter(
                        department_id=department_id
                    ).order_by('semester_number')
                )

            except:
                pass

        # SEMESTER FILTER
        if 'semester' in self.data:

            try:

                semester_id = int(
                    self.data.get('semester')
                )

                # ONLY LAB SUBJECTS
                self.fields['subject'].queryset = (
                    Subject.objects.filter(
                        semester_id=semester_id,
                        is_lab=True
                    ).order_by('name')
                )

            except:
                pass

        # EDIT MODE
        elif self.instance.pk:

            semester = self.instance.subject.semester

            self.fields['semester'].queryset = (
                Semester.objects.filter(
                    department=semester.department
                )
            )

            self.fields['subject'].queryset = (
                Subject.objects.filter(
                    semester=semester,
                    is_lab=True
                )
            )

            self.initial['department'] = (
                semester.department
            )

            self.initial['semester'] = semester
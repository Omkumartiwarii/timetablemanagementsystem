# Timetable Management System

A web-based **Timetable Management System** built with **Django** that automates timetable generation for educational institutions. The system helps administrators manage departments, semesters, subjects, faculty assignments, classrooms, and time slots while generating conflict-free class schedules.

---

## 📌 Overview

Managing academic timetables manually is time-consuming and prone to scheduling conflicts. This project provides an automated solution that:

- Generates timetables automatically
- Manages faculty, subjects, classrooms, and semesters
- Prevents timetable clashes
- Supports theory and laboratory sessions
- Provides separate dashboards for administrators, faculty, and students
- Allows timetable viewing and PDF export

---

## 🚀 Features

### Admin Module
- Department Management
- Semester Management
- Faculty Management
- Subject Management
- Classroom & Lab Management
- Time Slot Management
- Subject-Faculty Assignment
- Lab Room Assignment
- Recent Activity Tracking
- Automatic Timetable Generation
- Edit/Delete Timetable Entries

### Faculty Module
- Faculty Login
- View Today's Schedule
- View Weekly Timetable
- Assigned Subject Tracking

### Student Module
- Student Access Dashboard
- Department-wise Timetable View
- Semester-wise Timetable View
- Download Timetable as PDF

### Timetable Generation Engine
- Automatic schedule generation
- Faculty conflict prevention
- Classroom conflict prevention
- Semester conflict prevention
- Theory and Lab session support
- Room allocation optimization
- Faculty workload balancing

---

## 🏗️ System Architecture

### Core Entities

- Department
- Semester
- Faculty
- Subject
- Subject Faculty Mapping
- Classroom
- Time Slot
- Timetable
- Lab Room Mapping

### Relationships

```text
Department
    └── Semester
            └── Subject
                    └── Faculty

Semester
    └── Timetable

Classroom
    └── Timetable

TimeSlot
    └── Timetable



🛠️ Tech Stack
Backend
Python
Django 5.2
Database
SQLite (Default)
PostgreSQL Supported
Frontend
HTML
CSS
JavaScript
Bootstrap
Additional Libraries
Django REST Framework
Django Jazzmin
ReportLab
WhiteNoise
Gunicorn
Smart Selects

timetablemanagementsystem/
│
├── timetable_app/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── algorithms.py
│   └── management/
│
├── templates/
├── static/
├── media/
│
├── manage.py
├── requirements.txt
└── db.sqlite3


⚙️ Installation
1. Clone Repository
git clone https://github.com/your-username/timetable-management-system.git
cd timetable-management-system
2. Create Virtual Environment
python -m venv venv
Windows
venv\Scripts\activate
Linux/Mac
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Apply Migrations
python manage.py migrate
5. Create Superuser
python manage.py createsuperuser
6. Seed Sample Data (Optional)
python manage.py seed
7. Run Server
python manage.py runserver

Open:

http://127.0.0.1:8000
🔑 User Roles
Administrator

Responsible for:

Managing departments
Managing semesters
Managing faculty
Managing subjects
Managing classrooms
Managing timeslots
Generating timetables
Faculty

Can:

View assigned timetable
View daily schedule
View weekly schedule
Student

Can:

View semester timetable
Filter timetable
Download timetable PDF
🧠 Timetable Generation Logic

The timetable generation algorithm considers:

Hard Constraints
No faculty can teach two classes simultaneously
No classroom can be allocated twice at the same time
No semester can have overlapping classes
Lab sessions require consecutive slots
Lab subjects require assigned lab rooms
Optimization Goals
Balanced faculty workload
Reduced classroom switching
Efficient room utilization
Conflict-free scheduling
📄 PDF Export

The system supports timetable export using ReportLab.

Users can:

Generate timetable PDFs
Download semester schedules
Share printable timetables
📦 Requirements
Django==5.2.11
gunicorn==25.3.0
whitenoise==6.12.0
django-jazzmin==3.0.1
djangorestframework==3.16.1
pillow==12.1.1
requests==2.32.5
psycopg2-binary==2.9.11
reportlab==4.4.10
dj-database-url==3.0.1
django-smart-selects==1.7.2
python-dotenv
🔮 Future Enhancements
AI-assisted timetable optimization
Faculty preference scheduling
Attendance integration
Email notifications
REST API support
Mobile application
Multi-institute support
Analytics dashboard
🤝 Contributing
Fork the repository
Create a feature branch
git checkout -b feature-name
Commit changes
git commit -m "Added new feature"
Push branch
git push origin feature-name
Open a Pull Request
📜 License

This project is intended for educational and academic use. Feel free to modify and extend it according to your institution's requirements.

👨‍💻 Author

Om Kumar

Timetable Management System using Django for automated academic timetable generation and management.


This README is much more professional than the current one and accurately reflects the project's structure, models, routes, algorithm module, dashboards, and dependencies.

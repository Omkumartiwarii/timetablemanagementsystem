# 📅 TTGS — Timetable Generation System

A **Django-based automated Timetable Management System** for educational institutions.
Built by **Om Kumar** — automates conflict-free schedule generation across departments, semesters, faculty, and classrooms.

---

## 📌 Overview

Manual timetable creation is slow and error-prone. **TTGS** solves this by:

- Automatically generating conflict-free timetables using a **CSP (Constraint Satisfaction Problem)** algorithm
- Managing all academic entities: Departments, Semesters, Faculty, Subjects, Classrooms, Time Slots
- Supporting both **Theory** and **Laboratory** sessions
- Providing role-based dashboards for **Admin**, **Faculty**, and **Students**
- Enabling **PDF export** of generated timetables
- Including a built-in **AI Chatbot** for system guidance

---

## 🚀 Features

### 👨‍💼 Admin Module
- Manage Departments, Semesters, Faculty, Subjects, Classrooms, Time Slots
- Assign faculty to subjects (theory & lab — max 2 faculty per lab)
- Assign lab rooms to lab subjects
- Generate conflict-free timetables in one click
- Edit / Delete individual timetable entries (via AJAX)
- Track Recent Activity log with clear option

### 👨‍🏫 Faculty Module
- Login with assigned faculty credentials
- View today's schedule
- View full weekly timetable
- See all assigned subjects

### 🎓 Student Module
- Access timetable without login
- Filter by Department and Semester
- Download timetable as PDF (via ReportLab)

### 🤖 Built-in Chatbot (TTGS AI)
- Rule-based assistant embedded in all dashboards
- Answers role-specific questions (admin/faculty/student)
- Explains features like clash detection, CSP algorithm, lab scheduling, and PDF export

### ⚙️ Timetable Generation Engine
- **Hard Constraints** enforced:
  - No faculty double-booking
  - No classroom double-booking
  - No semester overlap
  - Lab subjects get consecutive slots
  - Lab subjects use assigned lab rooms only
- **Optimization**:
  - Balanced faculty workload (max 4 periods/day; max 2 theory + 1 lab)
  - Preferred classroom assignment per semester per shift (morning/afternoon)
  - Room switching minimized

---

## 🏗️ System Architecture

### Models

```
Department
    └── Semester
            └── Subject  (theory or lab, credits-based)
                    └── SubjectFaculty  (many-to-many; max 2 for labs)
                    └── SubjectLabRoom  (lab-subject → lab room mapping)

Faculty  (belongs to Department)

Classroom  (theory room or lab room)

TimeSlot  (Day + Start Time + End Time + Shift + Order + is_break)

Timetable  (Semester + Subject + Faculty M2M + Classroom + TimeSlot)

RecentActivity  (audit log of admin actions)
```

### Subject Logic (auto-calculated on save)
| Type | Credits | lectures_per_week | weekly_lab_sessions |
|---|---|---|---|
| Theory | Any | = credits | — |
| Lab | 2 | — | 1 |
| Lab | 3 | — | 2 |

### URL Structure

| URL | View | Access |
|---|---|---|
| `/` | Home page | Public |
| `/login/` | Role-based login | Public |
| `/logout/` | Logout | Authenticated |
| `/admin-dashboard/` | Admin dashboard | Admin |
| `/faculty-dashboard/` | Faculty schedule | Faculty |
| `/student-dashboard/` | Student timetable | Public |
| `/generate/` | Generate timetable | Admin |
| `/timetable/` | View full timetable | All |
| `/add-department/` | Add department | Admin |
| `/add-semester/` | Add semester | Admin |
| `/add-faculty/` | Add faculty | Admin |
| `/add-subject/` | Add subject | Admin |
| `/assign-subject/` | Assign faculty to subject | Admin |
| `/assign-lab-room/` | Assign lab room to subject | Admin |
| `/add-classroom/` | Add classroom/lab | Admin |
| `/add-timeslot/` | Add time slot | Admin |
| `/remove-timetable/` | Remove timetable entries | Admin |
| `/timetable/get/<id>/` | AJAX: get entry | Admin |
| `/timetable/save/` | AJAX: save entry | Admin |
| `/timetable/delete/<id>/` | AJAX: delete entry | Admin |
| `/ttgs-ai-chat/` | Chatbot view | All |
| `/teams/` | Teams/About page | Public |
| `/admin/` | Django admin panel | Superuser |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, Django 5.2 |
| Database | SQLite (default), PostgreSQL (supported) |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap |
| Admin UI | Django Jazzmin |
| PDF Export | ReportLab 4.4 |
| Static Files | WhiteNoise |
| Deployment | Gunicorn + Render / any WSGI host |
| Dynamic Forms | Django Smart Selects |
| Environment | python-dotenv |

---

## 📁 Project Structure

```
timetablemanagementsystem/
│
├── timetable_project/              # Django project config
│   ├── settings.py                 # All settings (DB, static, auth, timezone)
│   ├── urls.py                     # Root URL config
│   ├── wsgi.py
│   └── asgi.py
│
├── timetable_app/                  # Main application
│   ├── models.py                   # All database models
│   ├── views.py                    # All view functions (~1700 lines)
│   ├── forms.py                    # Django forms for data entry
│   ├── urls.py                     # App-level URL patterns
│   ├── algorithms.py               # Timetable generation engine (CSP)
│   ├── admin.py                    # Django admin registrations
│   ├── seed_data.py                # Sample data seeder
│   ├── apps.py
│   │
│   ├── management/
│   │   └── commands/
│   │       ├── seed.py             # `python manage.py seed`
│   │       └── fix_timeslot_order.py
│   │
│   ├── migrations/                 # 15 migration files (0001–0015)
│   │
│   ├── templates/                  # HTML templates
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── admin_dashboard.html
│   │   ├── faculty_dashboard.html
│   │   ├── student_dashboard.html
│   │   ├── timetable.html
│   │   ├── generate.html
│   │   ├── remove_timetable.html
│   │   ├── add_department.html
│   │   ├── add_semester.html
│   │   ├── add_faculty.html
│   │   ├── add_subject.html
│   │   ├── add_subject_faculty.html
│   │   ├── add_subject_lab_room.html
│   │   ├── add_classroom.html
│   │   ├── add_timeslot.html
│   │   └── teams.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   ├── home.css
│   │   │   ├── login.css
│   │   │   ├── style.css
│   │   │   ├── timetable.css
│   │   │   ├── templates.css
│   │   │   ├── faculty_dashboard.css
│   │   │   ├── student_dashboard.css
│   │   │   ├── chatbot.css
│   │   │   ├── footer.css
│   │   │   └── teams.css
│   │   ├── js/
│   │   │   ├── chatbot.js          # Rule-based AI chatbot
│   │   │   ├── timetable.js        # Timetable rendering & filters
│   │   │   ├── generate.js         # Generation progress UI
│   │   │   ├── admin_dashboard.js
│   │   │   ├── faculty_dashboard.js
│   │   │   ├── student_dashboard.js
│   │   │   ├── remove_timetable.js
│   │   │   ├── home.js
│   │   │   ├── login.js
│   │   │   ├── script.js
│   │   │   └── toggle.js
│   │   └── images/
│   │       ├── logo.png
│   │       └── (team member photos)
│   │
│   └── templatetags/
│       ├── custom_filters.py
│       └── custom_tags.py
│
├── manage.py
├── requirements.txt
├── Procfile                        # Render/Heroku deployment
├── queries                         # Useful PostgreSQL queries reference
├── data.json                       # Sample fixture data
├── timetable_data.json             # Timetable fixture
└── db.sqlite3                      # SQLite database (gitignored)
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip
- Git

### Step 1 — Clone the Repository

```bash
git clone https://github.com/om-kumar/timetable-management-system.git
cd timetable-management-system
```

### Step 2 — Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Create `.env` File

Create a `.env` file in the root directory (same level as `manage.py`):

```env
SECRET_KEY=your-very-secret-key-here
DEBUG=True
```

> **Note:** A default `SECRET_KEY` is already set in `settings.py` for development. For production, always override it via `.env`.

### Step 5 — Apply Migrations

```bash
python manage.py migrate
```

This runs all 15 migrations and sets up the full database schema.

### Step 6 — Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Enter a username, email (optional), and password. This account is used to log in as **Admin**.

### Step 7 — Seed Sample Data *(Optional but Recommended)*

```bash
python manage.py seed
```

This populates the database with:
- Sample departments, semesters, faculty
- Theory and lab subjects
- Classrooms and time slots
- Subject–faculty assignments

### Step 8 — Run the Development Server

```bash
python manage.py runserver
```

Open your browser at: **http://127.0.0.1:8000**

---

## 🔑 Login & User Roles

### How Login Works

TTGS uses Django's built-in authentication with **role-based redirection**:

| Role | Username | How to create |
|---|---|---|
| **Admin** | Any Django superuser | `python manage.py createsuperuser` |
| **Faculty** | `faculty_<name>` format | Created via Admin dashboard |
| **Student** | No login required | Access via `/student-dashboard/` |

On the login page, select your role (Admin / Faculty), enter credentials, and you'll be redirected to your dashboard.

### Default Admin Credentials (after createsuperuser)
Use whatever username and password you set during `createsuperuser`.

---

## 🧭 How to Use the System

### Step-by-step Admin Workflow

Follow this order when setting up from scratch:

```
1. Login as Admin
2. Add Department(s)         → /add-department/
3. Add Semester(s)           → /add-semester/
4. Add Faculty               → /add-faculty/
5. Add Subject(s)            → /add-subject/  (mark labs as "Is Lab")
6. Assign Faculty to Subject → /assign-subject/
7. Add Classroom(s)          → /add-classroom/ (mark labs as "Is Lab")
8. Add Time Slots            → /add-timeslot/  (set day, time, shift, order)
9. Assign Lab Rooms          → /assign-lab-room/ (only for lab subjects)
10. Generate Timetable       → /generate/
11. View Timetable           → /timetable/
```

### Timetable Generation

Go to `/generate/`, select the departments/semesters you want to generate for, and click **Generate**. The system will:
1. Load all subjects, faculty, classrooms, and time slots
2. Run the CSP algorithm with conflict checking
3. Store results in the `Timetable` model
4. Redirect to the timetable view

### PDF Export

On the Student Dashboard or Timetable view, click **Download PDF**. ReportLab generates a formatted PDF of the selected semester's timetable.

---

## 🧠 Timetable Generation Algorithm

The `algorithms.py` module implements a **Constraint Satisfaction Problem (CSP)** solver:

### Hard Constraints (must never be violated)

| Constraint | Rule |
|---|---|
| Faculty clash | No faculty teaches 2 classes at the same time |
| Classroom clash | No room is booked twice at the same time |
| Semester clash | No semester has 2 classes at the same time |
| Lab slots | Lab sessions require consecutive time slots |
| Lab rooms | Lab subjects must use their assigned lab room |

### Optimization

- **Faculty workload**: Max 4 periods/day; max 2 theory + 1 lab per day per faculty
- **Classroom assignment**: Each semester gets a preferred room per shift (morning/afternoon) via round-robin
- **Room switch penalty**: Minimizes unnecessary room changes for the same semester
- **Retry logic**: `MAX_RETRIES = 200` attempts per entry to find a valid slot

### Shift Detection

Time slots before **1:00 PM** → Morning shift  
Time slots from **1:00 PM** → Afternoon shift

---

## 🗄️ Database

### Default — SQLite

No configuration needed. Works out of the box.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Optional — PostgreSQL

Uncomment and configure in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ttgs_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then run:

```bash
pip install psycopg2-binary
python manage.py migrate
```

### Useful PostgreSQL Queries

Refer to the `queries` file in the project root for 25 ready-to-use SQL commands (view tables, insert, update, delete, reset, count, find duplicates, etc.).

---

## 🌐 Deployment (Render / Heroku)

The project includes a `Procfile` for WSGI deployment:

```
web: gunicorn timetable_project.wsgi
```

### Steps for Render

1. Push code to GitHub
2. Create a new **Web Service** on [render.com](https://render.com)
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `gunicorn timetable_project.wsgi`
5. Add environment variables:
   ```
   SECRET_KEY = <your-secret-key>
   DEBUG = False
   ```
6. Run migrations via Render Shell:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

WhiteNoise handles static files in production — no additional configuration needed.

---

## 📦 Requirements

```
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
```

---

## 🔮 Future Enhancements

- [ ] AI-assisted timetable optimization (genetic algorithm / ML)
- [ ] Faculty preference scheduling (preferred days/times)
- [ ] Attendance integration
- [ ] Email notifications for schedule changes
- [ ] Full REST API support
- [ ] Mobile application (React Native / Flutter)
- [ ] Multi-institute support
- [ ] Analytics dashboard (faculty load, room utilization)
- [ ] Google Calendar sync

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit
   ```bash
   git commit -m "Add: description of feature"
   ```
4. Push and open a Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

---

## 📜 License

This project is intended for educational and academic use. Free to modify and extend for your institution's requirements.

---

## 👨‍💻 Author

**Om Kumar**  
B.Tech Computer Science (Data Science) | Government Engineering College, Sheohar | 2026  
Internship Experience: Cisco · Salesforce · GRIP Program  

[GitHub](https://github.com/om-kumar) · [LinkedIn](https://linkedin.com/in/om-kumar)

> *TTGS — Automated academic timetable generation using Django and CSP algorithms.*

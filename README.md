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

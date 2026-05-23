//  TTGS CHATBOT — Admin / Faculty / Student  🔽

// CHAT TOGGLE

const chatToggleBtn = document.getElementById("chatToggleBtn");
const chatWindow = document.getElementById("chatWindow");
const chatClose = document.getElementById("cwClose");

chatToggleBtn.addEventListener("click", () => {
  chatWindow.classList.toggle("active");
  if (chatWindow.classList.contains("active")) {
    document.getElementById("cwInput").focus();
  }
});

chatClose.addEventListener("click", () => {
  chatWindow.classList.remove("active");
});

document.addEventListener("click", function (e) {
  const wrapper = document.querySelector(".chatbot-wrapper");
  if (!wrapper.contains(e.target)) {
    chatWindow.classList.remove("active");
  }
});

// MAIN CHAT LOGIC

(function () {
  "use strict";

  /* ── DOM ─────────────────────────────────────────── */
  const body = document.getElementById("cwBody");
  const input = document.getElementById("cwInput");
  const sendBtn = document.getElementById("cwSend");
  const clearBtn = document.getElementById("cwClear");

  /* ── ROLE DETECTION ──────────────────────────────────
     Add  data-role="admin" / "faculty" / "student"
     on your <body> tag in each Django template.
     e.g.  <body data-role="admin">
            <body data-role="faculty">
            <body data-role="student">
  ─────────────────────────────────────────────────── */
  const ROLE = (document.body.dataset.role || "admin").toLowerCase();

  /* ══════════════════════════════════════════════════
     SHARED RULES — apply to ALL roles
  ══════════════════════════════════════════════════ */
  const SHARED_RULES = [
    [
      [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
        "good night",
      ],
      [
        "Hello! 👋 How can I help you with TTGS today?",
        "Hi there! 👋 Ask me anything about timetables, subjects, classrooms, and more.",
        "Hey! 😊 Ready to help you with scheduling and timetable queries.",
      ],
    ],

    [
      ["how are you", "how r u", "what's up", "wassup"],
      [
        "I'm great and ready to help! 😊 What can I do for you?",
        "All good! 🤖 What do you need help with in TTGS?",
      ],
    ],

    [
      [
        "who are you",
        "what are you",
        "who made you",
        "who built you",
        "who created you",
        "introduce yourself",
        "your name",
      ],
      "🤖 I'm the TTGS Assistant — built into the Timetable Generation System.\nI can help you with timetables, faculty, subjects, classrooms, semesters, and scheduling!",
    ],

    [
      [
        "what is ttgs",
        "about ttgs",
        "explain ttgs",
        "about this system",
        "what can you do",
        "help me",
        "system features",
      ],
      "📘 TTGS (Timetable Generation System) is an automated scheduling platform.\n\n" +
        "✅ Generate conflict-free timetables automatically\n" +
        "👨‍🏫 Manage Faculty, Subjects, Classrooms & Semesters\n" +
        "⚠️ Detect and resolve scheduling clashes\n" +
        "📅 View per-department & per-faculty schedules\n\n" +
        "Ask me anything specific and I'll guide you!",
    ],

    [
      [
        "show clashes",
        "check conflict",
        "check clash",
        "faculty overlap",
        "room overlap",
        "conflict",
        "clash",
        "overlap",
        "how clash detection works",
        "is there any clash",
      ],
      "⚠️ TTGS has automatic clash detection built in:\n\n" +
        "• Faculty overlap — same teacher can't have 2 classes at once\n" +
        "• Room overlap — same room can't be double-booked\n" +
        "• Semester overlap — students can't have 2 classes at once\n\n" +
        "Clashes are resolved automatically during timetable generation. ✅",
    ],

    [
      [
        "what is csp",
        "constraint satisfaction",
        "csp algorithm",
        "how does csp work",
        "how timetable works",
        "how timetable generated",
      ],
      "🧠 CSP (Constraint Satisfaction Problem) is the algorithm TTGS uses to generate timetables.\n\n" +
        "It assigns classes to slots while satisfying:\n" +
        "• No faculty clash\n" +
        "• No room clash\n" +
        "• No semester clash\n" +
        "• Respect preferred timings\n\n" +
        "This ensures every timetable is conflict-free. ✅",
    ],

    [
      [
        "thank you",
        "thanks",
        "thx",
        "ty",
        "great",
        "awesome",
        "nice",
        "good job",
        "well done",
        "perfect",
      ],
      [
        "You're welcome! 😊 Feel free to ask anytime.",
        "Happy to help! 🤖 Let me know if you need anything else.",
        "Glad I could help! ✅",
      ],
    ],

    [
      ["bye", "goodbye", "see you", "take care", "quit", "exit"],
      [
        "Goodbye! 👋 Come back anytime.",
        "See you later! 😊 Have a great day.",
        "Take care! 👋",
      ],
    ],
  ];

  /* ══════════════════════════════════════════════════
     ADMIN RULES — Full system management access
  ══════════════════════════════════════════════════ */
  const ADMIN_RULES = [
    /* DASHBOARD */
    [
      [
        "show statistics",
        "show stats",
        "dashboard stats",
        "show dashboard",
        "open dashboard",
        "admin dashboard",
        "home",
      ],
      "📊 Your Admin Dashboard shows:\n" +
        "• Total Departments, Faculty, Subjects, Classrooms, Semesters\n" +
        "• Today's classes and recent activity log\n\n" +
        "Click 'Home' in the sidebar to go there anytime.",
    ],

    [
      [
        "show recent activities",
        "recent activity",
        "activity log",
        "what happened recently",
      ],
      "📋 Recent activities are shown on the right side of your Admin Dashboard.\nThey track every add, edit, delete, and generate action.",
    ],

    [
      ["clear recent activities", "clear activity", "delete activity log"],
      "🗑️ Admin Dashboard → Recent Activity panel → Click the 'Clear' button.",
    ],

    /* TIMETABLE — GENERATE */
    [
      [
        "generate all timetable",
        "generate all",
        "generate timetables",
        "generate for all departments",
      ],
      "⚙️ To generate timetables for ALL departments & semesters:\n" +
        "Sidebar → 'Generate Time Table' → Click 'Generate All'.\n\n" +
        "TTGS uses CSP algorithm to auto-resolve all clashes. ✅",
    ],

    [
      [
        "generate department timetable",
        "generate for department",
        "department timetable generate",
      ],
      "🏛️ To generate a timetable for a specific department:\n" +
        "Sidebar → 'Generate Time Table' → Select Department → Click Generate.",
    ],

    [
      [
        "generate semester timetable",
        "generate for semester",
        "semester timetable generate",
      ],
      "📖 To generate a timetable for a specific semester:\n" +
        "Sidebar → 'Generate Time Table' → Select Semester → Click Generate.",
    ],

    [
      [
        "generate timetable",
        "create timetable",
        "make timetable",
        "auto generate",
        "automatic timetable",
        "how to generate",
      ],
      "📅 To generate a timetable:\n" +
        "Sidebar → 'Generate Time Table'\n\n" +
        "Options:\n" +
        "• All departments — 'Generate All'\n" +
        "• Specific department or semester\n\n" +
        "TTGS auto-resolves all clashes using CSP. ✅",
    ],

    /* TIMETABLE — VIEW / EDIT / DELETE */
    [
      [
        "show today timetable",
        "today timetable",
        "today classes",
        "today schedule",
        "which class is now",
        "next class",
      ],
      "📅 Today's timetable is visible on your Admin Dashboard.\nIt shows all classes happening today across all departments.",
    ],

    [
      [
        "view timetable",
        "show timetable",
        "open timetable",
        "see timetable",
        "check timetable",
        "timetable",
        "time table",
      ],
      "📅 To view timetables:\nSidebar → 'View Timetable' → Select Department & Semester.",
    ],

    [
      [
        "edit timetable",
        "update timetable",
        "modify timetable",
        "change timetable",
        "add class",
        "delete class",
        "remove class",
      ],
      "✏️ To edit individual timetable entries:\n" +
        "Sidebar → 'View Timetable' → Find the entry → Click Edit or Delete.",
    ],

    [
      [
        "remove timetable",
        "delete timetable",
        "clear timetable",
        "remove all timetable",
        "delete all timetable",
      ],
      "🗑️ To remove timetable entries:\n" +
        "Sidebar → 'Remove Timetable' → Select Department & Semester → Remove.\n\n" +
        "⚠️ 'Remove All' clears the entire schedule for the selected dept/sem.",
    ],

    /* FACULTY */
    [
      [
        "add faculty",
        "add teacher",
        "add professor",
        "new faculty",
        "new teacher",
        "how to add faculty",
      ],
      "👨‍🏫 To add a new faculty member:\n" +
        "Sidebar → 'Teachers' → Click 'Add Teacher' → Fill in Name, Email, Department → Save.",
    ],

    [
      ["remove faculty", "delete faculty", "remove teacher", "delete teacher"],
      "🗑️ To remove a faculty member:\n" +
        "Sidebar → 'Teachers' → Find the faculty → Click Delete.",
    ],

    [
      ["edit faculty", "update faculty", "change faculty details"],
      "✏️ To edit faculty details:\n" +
        "Sidebar → 'Teachers' → Find the faculty → Click Edit → Update → Save.",
    ],

    [
      [
        "how many faculties",
        "how many teachers",
        "total faculty",
        "total teachers",
        "faculty count",
      ],
      "👨‍🏫 Total faculty count is on the Admin Dashboard stats panel.\nFull list: Sidebar → 'Teachers'.",
    ],

    [
      [
        "show all faculty",
        "faculty list",
        "all teachers",
        "staff list",
        "list of teachers",
      ],
      "👨‍🏫 Full faculty list:\nSidebar → 'Teachers'\n\nYou can add, edit, or delete faculty from there.",
    ],

    [
      [
        "faculty",
        "teacher",
        "professor",
        "staff",
        "open teachers section",
        "go to teachers",
      ],
      "👨‍🏫 Faculty management:\nSidebar → 'Teachers'\n\nAdd, edit, assign subjects, and remove faculty from there.",
    ],

    /* SUBJECTS */
    [
      ["add subject", "new subject", "create subject", "how to add subject"],
      "📚 To add a subject:\n" +
        "Sidebar → 'Subjects' → Click 'Add Subject' → Fill in:\n" +
        "• Subject Name\n• Semester\n• Credits\n• Lectures per Week\n• Is Lab? (Yes/No)\n\nClick Save.",
    ],

    [
      ["remove subject", "delete subject"],
      "🗑️ To remove a subject:\n" +
        "Sidebar → 'Subjects' → Find the subject → Click Delete.",
    ],

    [
      ["edit subject", "update subject", "change subject"],
      "✏️ To edit a subject:\n" +
        "Sidebar → 'Subjects' → Find the subject → Click Edit → Update → Save.",
    ],

    [
      [
        "assign subject",
        "assign faculty",
        "subject assignment",
        "faculty assignment",
        "how to assign",
      ],
      "📋 To assign a subject to a faculty:\n" +
        "Sidebar → 'Assign Subject' → Select Faculty & Subject → Click Save.\n\n" +
        "For lab subjects, up to 2 faculty members can be assigned.",
    ],

    [
      [
        "remove subject faculty",
        "delete assignment",
        "unassign subject",
        "remove assignment",
      ],
      "🗑️ To remove a subject-faculty assignment:\n" +
        "Sidebar → 'Assign Subject' → Find the assignment → Click Delete.",
    ],

    [
      [
        "how many subjects",
        "total subjects",
        "subject count",
        "show all subjects",
      ],
      "📚 Total subjects count is on the Admin Dashboard stats panel.\nFull list: Sidebar → 'Subjects'.",
    ],

    [
      [
        "what is lab subject",
        "lab subject",
        "is lab",
        "lab credits",
        "weekly lab sessions",
      ],
      "🔬 A lab subject in TTGS:\n" +
        "• Mark 'Is Lab' = Yes while adding a subject\n" +
        "• 2 credits → 1 lab session/week\n" +
        "• 3 credits → 2 lab sessions/week\n" +
        "• Up to 2 faculty can be assigned to a lab\n\n" +
        "Lab subjects are assigned to lab classrooms automatically.",
    ],

    [
      ["subject", "course", "paper", "open subject section", "go to subjects"],
      "📚 Subjects:\nSidebar → 'Subjects'\n\nAdd, edit, remove subjects and assign them to faculty.",
    ],

    /* DEPARTMENTS */
    [
      [
        "add department",
        "new department",
        "create department",
        "how to add department",
      ],
      "🏛️ To add a department:\n" +
        "Sidebar → 'Departments' → Click 'Add Department' → Enter Name → Save.",
    ],

    [
      ["remove department", "delete department"],
      "🗑️ To remove a department:\n" +
        "Sidebar → 'Departments' → Find the entry → Click Delete.\n\n" +
        "⚠️ Deleting a department removes all linked semesters, subjects, and faculty.",
    ],

    [
      ["how many departments", "total departments", "department count"],
      "🏛️ Total departments are on the Admin Dashboard stats panel.\nFull list: Sidebar → 'Departments'.",
    ],

    [
      [
        "department",
        "branch",
        "cse",
        "ece",
        "eee",
        "civil",
        "mechanical",
        "open departments section",
        "go to departments",
      ],
      "🏛️ Departments:\nSidebar → 'Departments'\n\nAdd, edit, and remove departments from there.",
    ],

    /* CLASSROOMS */
    [
      [
        "add classroom",
        "new classroom",
        "add room",
        "add lab room",
        "how to add classroom",
      ],
      "🏫 To add a classroom or lab:\n" +
        "Sidebar → 'Classrooms' → Click 'Add Classroom' → Fill in:\n" +
        "• Room Number\n• Capacity\n• Is Lab? (Yes/No)\n\nClick Save.",
    ],

    [
      [
        "remove classroom",
        "delete classroom",
        "remove room",
        "remove lab room",
      ],
      "🗑️ To remove a classroom:\n" +
        "Sidebar → 'Classrooms' → Find the entry → Click Delete.",
    ],

    [
      [
        "which classroom is free",
        "free classroom",
        "free room",
        "available room",
        "empty room",
      ],
      "🏫 To check free classrooms:\n" +
        "Sidebar → 'View Timetable' → Check which time slots have no class assigned for a room.",
    ],

    [
      ["how many classrooms", "total classrooms", "classroom count"],
      "🏫 Total classrooms are on the Admin Dashboard stats panel.\nFull list: Sidebar → 'Classrooms'.",
    ],

    [
      [
        "classroom",
        "room",
        "lab room",
        "open classroom section",
        "go to classrooms",
      ],
      "🏫 Classrooms & labs:\nSidebar → 'Classrooms'\n\nAdd, edit, and remove rooms from there.",
    ],

    /* SEMESTERS */
    [
      [
        "add semester",
        "new semester",
        "create semester",
        "how to add semester",
      ],
      "📖 To add a semester:\n" +
        "Sidebar → 'Semesters' → Click 'Add Semester' → Select Department → Enter Semester Number → Save.",
    ],

    [
      ["remove semester", "delete semester"],
      "🗑️ To remove a semester:\n" +
        "Sidebar → 'Semesters' → Find the entry → Click Delete.\n\n" +
        "⚠️ Deleting a semester removes all linked subjects.",
    ],

    [
      ["how many semesters", "total semesters", "semester count"],
      "📖 Total semesters are on the Admin Dashboard.\nFull list: Sidebar → 'Semesters'.",
    ],

    [
      ["semester", "sem", "open semester section", "go to semesters"],
      "📖 Semesters:\nSidebar → 'Semesters'\n\nAdd, edit, and remove semesters from there.",
    ],

    /* TIMESLOTS */
    [
      [
        "add timeslot",
        "new timeslot",
        "add time slot",
        "how to add timing",
        "add timing",
      ],
      "⏰ To add a time slot:\n" +
        "Sidebar → 'Timing' → Click 'Add Time Slot' → Fill in:\n" +
        "• Day (Monday–Saturday)\n• Start Time & End Time\n• Shift (Morning/Afternoon)\n• Is Break? (Yes/No)\n\nClick Save.",
    ],

    [
      [
        "remove timeslot",
        "delete timeslot",
        "remove time slot",
        "delete timing",
      ],
      "🗑️ To remove a time slot:\n" +
        "Sidebar → 'Timing' → Find the slot → Click Delete.",
    ],

    [
      ["what is break slot", "is break", "break timing", "lunch break"],
      "☕ Break slots are periods with no classes (e.g. lunch break).\n" +
        "When adding a time slot, check 'Is Break' to mark it.\n" +
        "TTGS will not assign classes to break slots.",
    ],

    [
      ["what is shift", "morning shift", "afternoon shift", "shift meaning"],
      "🌅 Each time slot belongs to a shift:\n" +
        "• Morning — early classes\n" +
        "• Afternoon — post-lunch classes\n\n" +
        "Shifts help organise the timetable display in order.",
    ],

    [
      [
        "timeslot",
        "timing",
        "time slot",
        "open timing section",
        "go to timing",
      ],
      "⏰ Time Slots:\nSidebar → 'Timing'\n\nAdd, edit, and remove time slots from there.",
    ],

    /* LOGIN / LOGOUT */
    [
      ["how to login", "login admin", "admin login"],
      "🔐 Admin Login:\n" +
        "Login page → Select 'Admin' tab → Enter Username & Password → Login.\n\n" +
        "Only staff users (is_staff=True in Django) can log in as Admin.",
    ],

    [
      ["logout", "how to logout", "sign out"],
      "⏻ To logout:\nClick 'Logout' at the bottom of the sidebar or top-right of the topbar.",
    ],
  ];

  /* ══════════════════════════════════════════════════
     FACULTY RULES — View-only: own schedule & subjects
  ══════════════════════════════════════════════════ */
  const FACULTY_RULES = [
    [
      [
        "show my timetable",
        "my timetable",
        "my schedule",
        "faculty timetable",
        "show my schedule",
      ],
      "📅 Your personal timetable is on your Faculty Dashboard.\n" +
        "Click 'Today' in the sidebar to see today's classes, or 'Week Schedule' for the full week.",
    ],

    [
      [
        "show today timetable",
        "today timetable",
        "today classes",
        "today schedule",
        "which class do i have now",
        "which class is now",
        "next class",
        "how many classes today",
      ],
      "📅 Your today's classes are in the 'Today' section of your Faculty Dashboard.\n" +
        "It shows subject, room, semester, and timing for each class.",
    ],

    [
      [
        "show weekly schedule",
        "weekly timetable",
        "this week classes",
        "weekly schedule",
        "week schedule",
      ],
      "📅 Your full weekly schedule is in the 'Week Schedule' section of your Faculty Dashboard.\n" +
        "Classes are sorted by day and time.",
    ],

    [
      ["tomorrow timetable", "tomorrow classes", "show tomorrow"],
      "📅 Check the 'Week Schedule' section of your Faculty Dashboard to see tomorrow's classes.",
    ],

    [
      [
        "show monday",
        "monday classes",
        "show tuesday",
        "tuesday classes",
        "show wednesday",
        "wednesday classes",
        "show thursday",
        "thursday classes",
        "show friday",
        "friday classes",
        "show saturday",
        "saturday classes",
      ],
      "📅 Go to 'Week Schedule' in your Faculty Dashboard to see classes for any specific day.\nClasses are listed by day in order.",
    ],

    [
      [
        "view timetable",
        "show timetable",
        "timetable",
        "time table",
        "schedule",
        "routine",
      ],
      "📅 Your timetable is on your Faculty Dashboard.\n" +
        "• 'Today' section — classes for today\n" +
        "• 'Week Schedule' section — full weekly view",
    ],

    [
      [
        "which subject am i teaching",
        "my subjects",
        "show my subjects",
        "what subjects do i teach",
        "my courses",
      ],
      "📚 Your assigned subjects are in the 'Subjects' section of your Faculty Dashboard.\n" +
        "It lists all subjects assigned to you with their semester info.",
    ],

    [
      [
        "which semester am i teaching",
        "my semester",
        "which department am i in",
      ],
      "🏛️ Your department and semester details are visible in the 'Subjects' section\n" +
        "and in the timetable entries on your Faculty Dashboard.",
    ],

    [
      [
        "which room is assigned to me",
        "my room",
        "room number for my class",
        "which classroom",
      ],
      "🏫 Your classroom for each class is shown in your today's timetable and weekly schedule.\n" +
        "Check the room column next to each subject.",
    ],

    [
      [
        "next class timing",
        "class timing",
        "subject timing",
        "free periods today",
        "free slot",
      ],
      "⏰ All class timings and free periods are visible in the 'Today' section of your Faculty Dashboard.",
    ],

    [
      ["lab schedule", "lab class", "when is my lab", "lab timing"],
      "🔬 Your lab sessions are part of your timetable.\n" +
        "Check 'Today' or 'Week Schedule' — lab subjects are listed with their room and timing.",
    ],

    [
      [
        "how to navigate",
        "sidebar options",
        "what sections",
        "menu options",
        "navigation",
      ],
      "📌 Your Faculty Dashboard has 3 sections:\n" +
        "• Today — classes for today\n" +
        "• Week Schedule — full weekly timetable\n" +
        "• Subjects — all your assigned subjects\n\n" +
        "Click each menu item to switch between sections.",
    ],

    [
      [
        "switch faculty",
        "select faculty",
        "change faculty",
        "which faculty am i",
      ],
      "👤 Select a faculty member from the dropdown at the top of the Faculty Dashboard.\n" +
        "All timetable and subject info updates for the selected faculty.",
    ],

    [
      ["how to login", "faculty login", "login faculty"],
      "🔐 Faculty Login:\n" +
        "Login page → Select 'Faculty' tab → Enter Username & Password → Login.",
    ],

    [
      ["logout", "sign out", "how to logout"],
      "⏻ To logout:\nClick 'Logout' at the bottom of the sidebar.",
    ],

    [
      ["what can i do", "my options", "help", "what can i see"],
      "👨‍🏫 As a Faculty member, you can:\n\n" +
        "📅 View today's classes — 'Today' section\n" +
        "📋 View weekly schedule — 'Week Schedule' section\n" +
        "📚 View your assigned subjects — 'Subjects' section\n\n" +
        "For changes to timetable or assignments, contact the Admin.",
    ],

    [
      [
        "i want to add",
        "can i add",
        "can i edit",
        "can i delete",
        "can i generate",
        "i want to generate",
      ],
      "ℹ️ Faculty accounts have view-only access.\n" +
        "To add, edit, or generate timetables — please contact the Admin.",
    ],
  ];

  /* ══════════════════════════════════════════════════
     STUDENT RULES — View timetable by dept & semester
  ══════════════════════════════════════════════════ */
  const STUDENT_RULES = [
    [
      [
        "show timetable",
        "view timetable",
        "see timetable",
        "check timetable",
        "my timetable",
        "class timetable",
      ],
      "📅 To view your timetable:\n" +
        "1. Select your Department from the dropdown\n" +
        "2. Select your Semester\n" +
        "3. The timetable loads automatically.\n\n" +
        "You can see subjects, faculty, room, and timings for each class.",
    ],

    [
      [
        "how to select department",
        "select department",
        "change department",
        "switch department",
      ],
      "🏛️ Use the Department dropdown at the top of the Student Dashboard.\n" +
        "Once selected, the Semester dropdown updates to show only that department's semesters.",
    ],

    [
      [
        "how to select semester",
        "select semester",
        "which semester",
        "change semester",
      ],
      "📖 After selecting your Department, use the Semester dropdown to filter your timetable.\n" +
        "The timetable grid will automatically update.",
    ],

    [
      [
        "show today timetable",
        "today timetable",
        "today classes",
        "today schedule",
        "which class is today",
        "next class",
      ],
      "📅 Select your Department & Semester, then check the current day column to see today's classes.\n" +
        "The grid shows all days from Monday to Saturday.",
    ],

    [
      [
        "show monday",
        "monday classes",
        "show tuesday",
        "tuesday classes",
        "show wednesday",
        "wednesday classes",
        "show thursday",
        "thursday classes",
        "show friday",
        "friday classes",
        "show saturday",
        "saturday classes",
      ],
      "📅 The timetable grid shows all days (Mon–Sat).\n" +
        "Select your Department & Semester to load the full weekly schedule.",
    ],

    [
      [
        "show weekly schedule",
        "weekly timetable",
        "weekly schedule",
        "full week schedule",
        "schedule",
        "routine",
      ],
      "📅 Your full weekly timetable (Mon–Sat) is shown in the grid on your Student Dashboard.\n" +
        "Select Department & Semester to load it.",
    ],

    [
      [
        "which teacher teaches",
        "who teaches my subject",
        "faculty for my class",
        "which professor",
        "who teaches",
      ],
      "👨‍🏫 Faculty details are shown inside each cell of the timetable grid.\n" +
        "Select your Department & Semester to see subject-wise faculty assignments.",
    ],

    [
      [
        "which room",
        "classroom for my class",
        "room number",
        "where is my class",
        "which classroom",
      ],
      "🏫 Room details are shown in each class cell of the timetable grid.\n" +
        "Select your Department & Semester to view the full schedule with rooms.",
    ],

    [
      [
        "which subjects do i have",
        "my subjects",
        "subject list",
        "what subjects",
        "show subjects",
      ],
      "📚 All your subjects for the selected Semester are visible in the timetable grid.\n" +
        "Select your Department & Semester to load them.",
    ],

    [
      ["lab class", "lab schedule", "which lab", "lab timing", "lab subject"],
      "🔬 Lab classes are included in your timetable grid.\n" +
        "They show the assigned lab room and timing.\n" +
        "Select your Department & Semester to see all lab timings.",
    ],

    [
      [
        "show all departments",
        "all departments",
        "which departments",
        "list of departments",
      ],
      "🏛️ All available departments are listed in the Department dropdown.\n" +
        "Click it to see all departments and select yours.",
    ],

    [
      [
        "show all semesters",
        "which semesters",
        "semester list",
        "all semesters",
      ],
      "📖 Semesters appear in the Semester dropdown after you select a Department.\n" +
        "Only semesters for the selected department are shown.",
    ],

    [
      ["how to login", "student login", "login student", "how to access"],
      "🔐 Student Login:\n" +
        "Login page → Select 'Student' tab → Enter your Enrollment Number → Click Login.\n\n" +
        "No password needed — just your enrollment number.",
    ],

    [
      ["logout", "sign out", "how to logout"],
      "⏻ To logout:\nScroll to the bottom of the page and click 'Logout'.",
    ],

    [
      [
        "what can i do",
        "my options",
        "help",
        "what can i see",
        "student features",
      ],
      "🎓 As a Student, you can:\n\n" +
        "📅 View your timetable by selecting Department & Semester\n" +
        "👨‍🏫 See which faculty teaches each subject\n" +
        "🏫 Check which room each class is held in\n" +
        "🔬 View lab schedules too\n\n" +
        "Select your Department & Semester to get started!",
    ],

    [
      [
        "i want to add",
        "can i add",
        "can i edit",
        "can i delete",
        "can i change timetable",
      ],
      "ℹ️ Student accounts have view-only access.\n" +
        "For any changes, please contact the Admin.",
    ],

    [
      ["what is enrollment", "enrollment number", "what to enter in login"],
      "🎓 Your enrollment number is your unique student ID.\n" +
        "Enter it on the Student login tab to access your dashboard — no password needed.",
    ],
  ];

  /* ── DEFAULT REPLIES ──────────────────────────── */
  const DEFAULT_REPLIES = {
    admin: [
      "🤖 I'm not sure about that. Try asking about:\n• Timetable generation or management\n• Faculty, Subjects, Classrooms, Departments, Semesters\n• Timing slots or clash detection",
      "💡 I can help with:\ntimetable, faculty, subjects, classrooms, semesters, timings, clashes.\nPlease rephrase your question!",
      "📘 Hmm, I didn't get that. Try:\n'How to generate timetable?' or 'How to add faculty?'",
    ],
    faculty: [
      "🤖 I'm not sure about that. Try asking about:\n• Today's classes or weekly schedule\n• Your assigned subjects\n• Room or timing details",
      "💡 As Faculty, I can help with:\nmy timetable, today's classes, week schedule, my subjects, my room.\nPlease rephrase!",
      "📘 Hmm, I didn't get that. Try:\n'Show my today timetable' or 'Which subject am I teaching?'",
    ],
    student: [
      "🤖 I'm not sure about that. Try asking about:\n• Your timetable\n• Selecting Department & Semester\n• Faculty or room details",
      "💡 As a Student, I can help with:\ntimetable, subjects, faculty, rooms, lab schedule.\nPlease rephrase!",
      "📘 Hmm, I didn't get that. Try:\n'Show my timetable' or 'How to select semester?'",
    ],
  };

  /* ── WELCOME MESSAGES ─────────────────────────── */
  const WELCOME = {
    admin:
      "Hi Admin! 👋 I'm the TTGS Assistant.\nAsk me about timetable generation, faculty, subjects, classrooms, semesters, or timings!",
    faculty:
      "Hi! 👋 I'm the TTGS Faculty Assistant.\nAsk me about your today's classes, weekly schedule, or assigned subjects!",
    student:
      "Hi! 👋 I'm the TTGS Student Assistant.\nSelect your Department & Semester to view your timetable.\nAsk me anything!",
  };

  /* ── ACTIVE RULE SET ──────────────────────────── */
  const ROLE_RULES = {
    admin: [...ADMIN_RULES, ...SHARED_RULES],
    faculty: [...FACULTY_RULES, ...SHARED_RULES],
    student: [...STUDENT_RULES, ...SHARED_RULES],
  };

  const ACTIVE_RULES = ROLE_RULES[ROLE] || ROLE_RULES.admin;
  const ACTIVE_DEFAULTS = DEFAULT_REPLIES[ROLE] || DEFAULT_REPLIES.admin;

  /* ── MATCH ENGINE ─────────────────────────────── */
  function getReply(msg) {
    const m = msg.trim().toLowerCase();
    let bestReply = null;
    let bestLen = 0;

    for (const [keywords, reply] of ACTIVE_RULES) {
      for (const kw of keywords) {
        if (m.includes(kw) && kw.length > bestLen) {
          bestLen = kw.length;
          bestReply = reply;
        }
      }
    }

    const reply =
      bestReply ||
      ACTIVE_DEFAULTS[Math.floor(Math.random() * ACTIVE_DEFAULTS.length)];

    return Array.isArray(reply)
      ? reply[Math.floor(Math.random() * reply.length)]
      : reply;
  }

  /* ── RENDER HELPERS ───────────────────────────── */
  function getTime() {
    return new Date().toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  function escHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function appendMsg(text, who) {
    const row = document.createElement("div");
    row.className = "msg-row " + who;

    const avatar = document.createElement("div");
    avatar.className = "msg-avatar" + (who === "user" ? " user" : "");
    avatar.textContent = who === "bot" ? "🤖" : "👤";

    const inner = document.createElement("div");
    inner.className = "msg-inner";

    const bubble = document.createElement("div");
    bubble.className = "msg-bubble " + who;
    bubble.innerHTML = escHtml(text).replace(/\n/g, "<br>");

    const time = document.createElement("div");
    time.className = "msg-time";
    time.textContent = getTime();

    inner.appendChild(bubble);
    inner.appendChild(time);

    if (who === "bot") {
      row.appendChild(avatar);
      row.appendChild(inner);
    } else {
      row.appendChild(inner);
      row.appendChild(avatar);
    }

    body.appendChild(row);
    body.scrollTop = body.scrollHeight;
  }

  function showTyping() {
    const row = document.createElement("div");
    row.className = "msg-row bot";
    row.id = "typingRow";

    const avatar = document.createElement("div");
    avatar.className = "msg-avatar";
    avatar.textContent = "🤖";

    const bubble = document.createElement("div");
    bubble.className = "typing-bubble";
    bubble.innerHTML = "<span></span><span></span><span></span>";

    row.appendChild(avatar);
    row.appendChild(bubble);
    body.appendChild(row);
    body.scrollTop = body.scrollHeight;
  }

  function removeTyping() {
    const el = document.getElementById("typingRow");
    if (el) el.remove();
  }

  /* ── SEND ─────────────────────────────────────── */
  let busy = false;

  function send() {
    const text = input.value.trim();
    if (!text || busy) return;

    busy = true;
    sendBtn.disabled = true;
    appendMsg(text, "user");
    input.value = "";
    input.focus();
    showTyping();

    setTimeout(() => {
      removeTyping();
      appendMsg(getReply(text), "bot");
      busy = false;
      sendBtn.disabled = false;
    }, 550);
  }

  sendBtn.addEventListener("click", send);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });

  /* ── CLEAR ────────────────────────────────────── */
  clearBtn.addEventListener("click", () => {
    body.innerHTML = `
      <div class="welcome-card">
        <div class="wc-icon">👋</div>
        <h4>Welcome to TTGS Assistant</h4>
        <p>Ask me anything about timetable generation, faculty,<br>subjects, classrooms, semesters, and more!</p>
      </div>`;
  });

  /* ── AUTO WELCOME ─────────────────────────────── */
  setTimeout(() => {
    appendMsg(WELCOME[ROLE] || WELCOME.admin, "bot");
  }, 400);
})();

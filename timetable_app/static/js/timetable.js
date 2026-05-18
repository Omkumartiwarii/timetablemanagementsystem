var allSchedules = JSON.parse(
  document.getElementById("allSchedulesData").textContent,
);

var WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

var todayIndex = WEEK.indexOf(TODAY_NAME);

if (todayIndex === -1) {
  todayIndex = 0;
}

var dayOffset = 0;

// ======================================
// HELPERS
// ======================================

function getMinOffset() {
  return -todayIndex;
}

function getMaxOffset() {
  return WEEK.length - 1 - todayIndex;
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ======================================
// TOAST
// ======================================

function showToast(msg, type) {
  var toast = document.getElementById("ttToast");
  var icon = document.getElementById("toastIcon");
  var text = document.getElementById("toastMsg");

  toast.className = "";

  if (type === "success") {
    toast.classList.add("toast-success");
    icon.className = "fa-solid fa-circle-check";
  } else if (type === "error") {
    toast.classList.add("toast-error");
    icon.className = "fa-solid fa-circle-xmark";
  } else {
    toast.classList.add("toast-info");
    icon.className = "fa-solid fa-circle-info";
  }

  text.textContent = msg;

  toast.classList.add("show");

  setTimeout(function () {
    toast.classList.remove("show");
  }, 3000);
}

// ======================================
// TODAY RENDER
// ======================================

function renderDay(offset) {
  var idx = todayIndex + offset;

  var dayName = WEEK[idx];

  var items = allSchedules[dayName] || [];

  var count = items.length;

  var relLabel =
    offset === 0
      ? "TODAY"
      : offset === -1
        ? "YESTERDAY"
        : offset === 1
          ? "TOMORROW"
          : dayName.toUpperCase();

  document.getElementById("bannerDayLabel").textContent = relLabel;

  document.getElementById("bannerDayName").textContent =
    "🗓️ " + dayName + "'s Classes";

  document.getElementById("bannerBadge").textContent =
    "Total: " + count + (count === 1 ? " Class" : " Classes");

  document.getElementById("prevDayLabel").textContent =
    idx - 1 >= 0 ? WEEK[idx - 1] : "";

  document.getElementById("nextDayLabel").textContent =
    idx + 1 <= WEEK.length - 1 ? WEEK[idx + 1] : "";

  document.getElementById("prevBtn").disabled = offset <= getMinOffset();

  document.getElementById("nextBtn").disabled = offset >= getMaxOffset();

  var body = document.getElementById("todayBody");

  if (count === 0) {
    body.innerHTML =
      '<div class="no-today anim-fade">' +
      '<div class="no-today-icon">📭</div>' +
      "No classes scheduled for " +
      dayName +
      "</div>";

    return;
  }

  var cards = items
    .map(function (item, i) {
      return (
        '<div class="class-card">' +
        '<div class="card-accent"></div>' +
        '<div class="card-num">' +
        '<div class="card-num-circle">' +
        (i + 1) +
        "</div>" +
        "</div>" +
        '<div class="card-main">' +
        '<div class="card-subject">' +
        escHtml(item.subject) +
        "</div>" +
        '<div class="card-tags">' +
        '<span class="ctag ctag-time">' +
        '<span class="ctag-icon">🕒</span>' +
        escHtml(item.time) +
        "</span>" +
        '<span class="ctag ctag-sem">' +
        '<span class="ctag-icon">🏫</span>' +
        escHtml(item.semester) +
        "</span>" +
        '<span class="ctag ctag-room">' +
        '<span class="ctag-icon">🚪</span>' +
        escHtml(item.room) +
        "</span>" +
        '<span class="ctag ctag-faculty">' +
        '<span class="ctag-icon">👨‍🏫</span>' +
        escHtml(item.faculty) +
        "</span>" +
        "</div>" +
        "</div>" +
        "</div>"
      );
    })
    .join("");

  body.innerHTML = '<div class="anim-fade">' + cards + "</div>";
}

// ======================================
// DAY NAVIGATION
// ======================================

function changeDay(dir) {
  var newOff = dayOffset + dir;

  if (newOff < getMinOffset() || newOff > getMaxOffset()) {
    return;
  }

  dayOffset = newOff;

  renderDay(dayOffset);
}

// ======================================
// SECTION TOGGLE
// ======================================

function showToday() {
  dayOffset = 0;

  renderDay(0);

  document.getElementById("todaySection").style.display = "block";

  document.getElementById("filterFormSection").style.display = "none";

  document.getElementById("fullSection").style.display = "none";

  document.getElementById("todayBtn").classList.add("active-btn");

  document.getElementById("filterBtn").classList.remove("active-btn");
}

function showFilter() {
  document.getElementById("filterFormSection").style.display = "block";

  document.getElementById("todaySection").style.display = "none";

  var hasTable = document.querySelector("#fullSection .table-card");

  document.getElementById("fullSection").style.display = hasTable
    ? "block"
    : "none";

  document.getElementById("filterBtn").classList.add("active-btn");

  document.getElementById("todayBtn").classList.remove("active-btn");
}

// ======================================
// FILTER SEMESTERS
// ======================================

var deptSelect = document.querySelector('select[name="department"]');

var semSelect = document.querySelector('select[name="semester"]');

var allSemesterOptions = Array.from(semSelect.options);

function filterSemesters() {
  var selectedDept = deptSelect.value;

  semSelect.innerHTML = "";

  allSemesterOptions.forEach(function (option) {
    if (option.value === "all") {
      semSelect.appendChild(option.cloneNode(true));

      return;
    }

    var text = option.textContent;

    if (
      selectedDept === "all" ||
      text.includes(deptSelect.options[deptSelect.selectedIndex].text)
    ) {
      semSelect.appendChild(option.cloneNode(true));
    }
  });
}

deptSelect.addEventListener("change", filterSemesters);

// ======================================
// PAGE LOAD
// ======================================

window.addEventListener("DOMContentLoaded", function () {
  filterSemesters();

  document.getElementById("todaySection").style.display = "none";

  document.getElementById("filterFormSection").style.display = "none";

  document.getElementById("fullSection").style.display = "none";

  document.getElementById("todayBtn").classList.remove("active-btn");

  document.getElementById("filterBtn").classList.remove("active-btn");

  if (SERVER_SECTION === "filter") {
    showFilter();
  }
});

// ======================================
// MODAL
// ======================================

function openAddModal(day, slot, semesterId) {
  document.getElementById("entryId").value = "";

  document.getElementById("dayField").value = day;

  document.getElementById("slotField").value = slot;

  document.getElementById("semesterField").value = semesterId;

  document.getElementById("modalTitle").innerHTML =
    '<i class="fa-solid fa-calendar-plus"></i> Add Class';

  document.getElementById("ttModal").classList.add("open");
}

function closeModal() {
  document.getElementById("ttModal").classList.remove("open");
}

function openEditModal(id) {
  fetch("/timetable/get/" + id + "/")
    .then(function (res) {
      return res.json();
    })

    .then(function (data) {
      document.getElementById("entryId").value = data.id;

      document.getElementById("subjectField").value = data.subject;

      document.getElementById("facultyField").value = data.faculty;

      document.getElementById("roomField").value = data.room;

      document.getElementById("dayField").value = data.day;

      document.getElementById("slotField").value = data.slot;

      document.getElementById("semesterField").value = data.semester;

      document.getElementById("modalTitle").innerHTML =
        '<i class="fa-solid fa-pen-to-square"></i> Edit Class';

      document.getElementById("ttModal").classList.add("open");
    });
}

// ======================================
// SAVE ENTRY
// ======================================

function submitForm() {
  fetch("/timetable/save/", {
    method: "POST",

    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },

    body: JSON.stringify({
      id: document.getElementById("entryId").value,

      day: document.getElementById("dayField").value,

      slot: document.getElementById("slotField").value,

      subject: document.getElementById("subjectField").value,

      faculty: document.getElementById("facultyField").value,

      room: document.getElementById("roomField").value,

      semester: document.getElementById("semesterField").value,
    }),
  })
    .then(function (res) {
      return res.json();
    })

    .then(function (data) {
      closeModal();

      var isEdit = !!document.getElementById("entryId").value;

      showToast(
        isEdit ? "Class updated successfully!" : "Class added successfully!",
        "success",
      );

      setTimeout(function () {
        location.reload();
      }, 1500);
    })

    .catch(function () {
      showToast("Something went wrong. Please try again.", "error");
    });
}

// ======================================
// DELETE
// ======================================

var pendingDeleteId = null;

function confirmDelete(id) {
  pendingDeleteId = id;

  document.getElementById("ttConfirm").classList.add("open");
}

function closeConfirm() {
  pendingDeleteId = null;

  document.getElementById("ttConfirm").classList.remove("open");
}

document.getElementById("confirmYesBtn").addEventListener("click", function () {
  if (!pendingDeleteId) return;

  var deleteId = pendingDeleteId;

  closeConfirm();

  fetch("/timetable/delete/" + deleteId + "/", {
    method: "POST",

    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then(function (res) {
      return res.json();
    })

    .then(function () {
      showToast("Class deleted successfully!", "success");

      setTimeout(function () {
        location.reload();
      }, 1500);
    })

    .catch(function () {
      showToast("Delete failed. Please try again.", "error");
    });
});

// ======================================
// CSRF
// ======================================

function getCookie(name) {
  var cookieValue = null;

  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();

      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

        break;
      }
    }
  }

  return cookieValue;
}

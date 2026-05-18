const form = document.getElementById("removeForm");
const loader = document.getElementById("loader");
const confirmModal = document.getElementById("confirmModal");
const confirmBtn = document.getElementById("confirmBtn");
const cancelBtn = document.getElementById("cancelBtn");
const removeType = document.getElementById("removeType");
const departmentSelect = document.getElementById("departmentSelect");
const semesterSelect = document.getElementById("semesterSelect");
const departmentLabel = document.getElementById("departmentLabel");
const semesterLabel = document.getElementById("semesterLabel");

let formSubmitted = false;

// ===== SHOW / HIDE FIELDS =====

function toggleFields() {
  const type = removeType.value;

  if (type === "all") {
    departmentLabel.style.display = "none";
    departmentSelect.style.display = "none";

    semesterLabel.style.display = "none";
    semesterSelect.style.display = "none";
  } else if (type === "department") {
    departmentLabel.style.display = "block";
    departmentSelect.style.display = "block";

    semesterLabel.style.display = "none";
    semesterSelect.style.display = "none";
  } else if (type === "semester") {
    departmentLabel.style.display = "block";
    departmentSelect.style.display = "block";

    semesterLabel.style.display = "block";
    semesterSelect.style.display = "block";
  }
}

removeType.addEventListener("change", toggleFields);

toggleFields();

// ===== FILTER SEMESTERS =====

const allSemesterOptions = Array.from(
  semesterSelect.querySelectorAll("option"),
);

function filterSemesters() {
  const selectedDept =
    departmentSelect.options[departmentSelect.selectedIndex]?.text;

  semesterSelect.innerHTML = '<option value="">---------</option>';

  allSemesterOptions.forEach((option) => {
    if (!option.value) return;

    if (option.dataset.department === selectedDept) {
      semesterSelect.appendChild(option.cloneNode(true));
    }
  });
}

departmentSelect.addEventListener("change", filterSemesters);

// ===== OPEN MODAL =====

form.addEventListener("submit", function (e) {
  const type = removeType.value;

  if (type === "department" && !departmentSelect.value) {
    alert("Please select a department");

    e.preventDefault();

    return;
  }

  if (type === "semester") {
    if (!departmentSelect.value) {
      alert("Please select a department");

      e.preventDefault();

      return;
    }

    if (!semesterSelect.value) {
      alert("Please select a semester");

      e.preventDefault();

      return;
    }
  }

  if (!formSubmitted) {
    e.preventDefault();

    confirmModal.classList.add("show");
  }
});

// ===== CANCEL =====

cancelBtn.addEventListener("click", function () {
  confirmModal.classList.remove("show");
});

// ===== CONFIRM REMOVE =====

confirmBtn.addEventListener("click", function () {
  confirmModal.classList.remove("show");

  loader.classList.add("show");

  formSubmitted = true;

  form.submit();
});

// ===== AUTO HIDE TOAST =====

const toast = document.getElementById("toast");

if (toast) {
  setTimeout(() => {
    toast.style.display = "none";
  }, 3000);
}

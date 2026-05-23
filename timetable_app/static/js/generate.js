// ===== CONDITIONAL FIELDS =====
const generateType = document.getElementById("generateType");

const departmentField = document.getElementById("departmentField");

const semesterField = document.getElementById("semesterField");

const semesterDepartment = document.getElementById("semesterDepartment");

const semesterSelect = document.getElementById("semesterSelect");

function toggleFields() {
  const value = generateType.value;

  departmentField.style.display = value === "department" ? "block" : "none";

  semesterField.style.display = value === "semester" ? "block" : "none";
}

generateType.addEventListener("change", toggleFields);

toggleFields();

// ===== FILTER SEMESTER BY DEPARTMENT =====
semesterDepartment.addEventListener("change", function () {
  const selectedDept = this.value;

  const options = semesterSelect.querySelectorAll("option");

  semesterSelect.value = "";

  options.forEach((option) => {
    if (!option.dataset.department) {
      option.style.display = "block";
      return;
    }

    if (option.dataset.department === selectedDept) {
      option.style.display = "block";
    } else {
      option.style.display = "none";
    }
  });
});

// ===== FORM SUBMIT =====
document
  .getElementById("generateForm")
  .addEventListener("submit", function (e) {
    const type = generateType.value;

    const deptSelect = document.querySelector('select[name="department"]');

    const semSelect = document.querySelector('select[name="semester"]');

    if (type === "department" && !deptSelect.value) {
      alert("Please select a department");

      e.preventDefault();

      return;
    }

    if (type === "semester") {
      if (!semesterDepartment.value) {
        alert("Please select a department");

        e.preventDefault();

        return;
      }

      if (!semSelect.value) {
        alert("Please select a semester");

        e.preventDefault();

        return;
      }
    }

    document.getElementById("loader").classList.add("show");
  });

// ===== AUTO HIDE SUCCESS TOAST =====
document.querySelectorAll(".toast-success").forEach(function (toast) {
  setTimeout(function () {
    toast.remove();
  }, 4000);
});

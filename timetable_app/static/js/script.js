// ===== ALERT ON GENERATE =====
function showGenerateAlert() {
    alert("Timetable generated successfully!");
}

// ===== CONFIRM DELETE =====
function confirmDelete() {
    return confirm("Are you sure you want to delete timetable?");
}

// ===== FILTER AUTO SUBMIT =====
function autoSubmit() {
    document.getElementById("filterForm").submit();
}

// ===== HIGHLIGHT CELL ON CLICK =====
document.addEventListener("DOMContentLoaded", function () {
    let cells = document.querySelectorAll("td");

    cells.forEach(cell => {
        cell.addEventListener("click", function () {
            this.style.backgroundColor = "#dff0d8";
        });
    });
});
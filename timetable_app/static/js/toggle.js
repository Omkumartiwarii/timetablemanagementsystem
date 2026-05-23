function toggleMenu() {
  const sidebar = document.querySelector(".sidebar");
  const btn = document.getElementById("menuBtn");
  const overlay = document.getElementById("overlay");

  const isOpen = sidebar.classList.toggle("active");
  overlay.classList.toggle("active");

  // 🔥 SCROLL LOCK
  document.body.classList.toggle("no-scroll", isOpen);

  btn.textContent = isOpen ? "✖" : "☰";
}

document.getElementById("overlay").addEventListener("click", function () {
  const sidebar = document.querySelector(".sidebar");
  const btn = document.getElementById("menuBtn");

  sidebar.classList.remove("active");
  this.classList.remove("active");

  // 🔥 SCROLL UNLOCK
  document.body.classList.remove("no-scroll");

  btn.textContent = "☰";
});

// Delete Modal Functions

function openDeleteModal(deleteUrl) {
  document.getElementById("deleteModal").style.display = "flex";

  document.getElementById("confirmDeleteBtn").href = deleteUrl;
}

function closeDeleteModal() {
  document.getElementById("deleteModal").style.display = "none";
}

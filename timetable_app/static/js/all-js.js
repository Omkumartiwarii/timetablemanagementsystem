function toggleMenu() {
  const sidebar = document.querySelector(".sidebar");
  const btn = document.getElementById("menuBtn");
  const overlay = document.getElementById("overlay");

  const isOpen = sidebar.classList.toggle("active");
  overlay.classList.toggle("active");

  if (isOpen) {
    btn.textContent = "✖";
  } else {
    btn.textContent = "☰";
  }
}

document.getElementById("overlay").addEventListener("click", function () {
  const sidebar = document.querySelector(".sidebar");
  const btn = document.getElementById("menuBtn");

  sidebar.classList.remove("active");
  this.classList.remove("active");

  btn.textContent = "☰";
});

const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");
const hamburger = document.getElementById("hamburgerBtn");

if (hamburger && sidebar && overlay) {
  hamburger.addEventListener("click", () => {
    sidebar.classList.toggle("active");
    overlay.classList.toggle("active");
  });
}

if (overlay && sidebar) {
  overlay.addEventListener("click", () => {
    sidebar.classList.remove("active");
    overlay.classList.remove("active");
  });
}

const menuLinks = document.querySelectorAll(".menu-link");
const sections = document.querySelectorAll(".page-section");

menuLinks.forEach((link) => {
  link.addEventListener("click", function (e) {
    e.preventDefault();
    menuLinks.forEach((l) => l.classList.remove("active"));
    this.classList.add("active");

    const target = this.getAttribute("data-target");
    sections.forEach((s) => s.classList.remove("active"));
    const ts = document.getElementById(target);
    if (ts) ts.classList.add("active");

    if (window.innerWidth <= 900) {
      sidebar.classList.remove("active");
      overlay.classList.remove("active");
    }
  });
});

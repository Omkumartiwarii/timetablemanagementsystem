// ── CAROUSEL ──
const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");
let idx = 0,
  timer;

function showSlide(i) {
  slides.forEach((s, j) => s.classList.toggle("active", j === i));
  dots.forEach((d, j) => d.classList.toggle("active", j === i));
}

function nextSlide() {
  idx = (idx + 1) % slides.length;
  showSlide(idx);
}
function startAuto() {
  clearInterval(timer);
  timer = setInterval(nextSlide, 5500);
}
function stopAuto() {
  clearInterval(timer);
}

window.currentSlide = (i) => {
  idx = i;
  showSlide(i);
  stopAuto();
  startAuto();
};

const carousel = document.querySelector(".hero-right");
if (carousel) {
  carousel.addEventListener("mouseenter", stopAuto);
  carousel.addEventListener("mouseleave", startAuto);
}
showSlide(0);
startAuto();

// ── HAMBURGER ──
const toggle = document.getElementById("menuToggle");
const mobileMenu = document.getElementById("mobileMenu");
const overlay = document.getElementById("overlay");

function openMenu() {
  toggle.classList.add("open");
  toggle.setAttribute("aria-expanded", "true");
  mobileMenu.classList.add("open");
  mobileMenu.setAttribute("aria-hidden", "false");
  overlay.classList.add("active");
  document.body.style.overflow = "hidden";
}
function closeMenu() {
  toggle.classList.remove("open");
  toggle.setAttribute("aria-expanded", "false");
  mobileMenu.classList.remove("open");
  mobileMenu.setAttribute("aria-hidden", "true");
  overlay.classList.remove("active");
  document.body.style.overflow = "";
}

if (toggle && mobileMenu) {
  toggle.addEventListener("click", () =>
    mobileMenu.classList.contains("open") ? closeMenu() : openMenu(),
  );
  mobileMenu
    .querySelectorAll("a")
    .forEach((a) => a.addEventListener("click", closeMenu));
  overlay.addEventListener("click", closeMenu);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMenu();
  });
  window.addEventListener("resize", () => {
    if (window.innerWidth > 768) closeMenu();
  });
}

// ── NAVBAR SCROLL ──
const navbar = document.getElementById("navbar");
window.addEventListener(
  "scroll",
  () => {
    navbar.classList.toggle("scrolled", window.scrollY > 50);
  },
  { passive: true },
);

// ── FADE UP ANIMATIONS ──
const obs = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        obs.unobserve(e.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: "0px 0px -40px 0px" },
);
document.querySelectorAll(".fade-up").forEach((el) => obs.observe(el));

// ── CONTACT FORM (frontend demo) ──
function handleFormSubmit(btn) {
  btn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Sending...';
  btn.style.opacity = "0.7";
  setTimeout(() => {
    btn.innerHTML = '<i class="fa-solid fa-check"></i> Message Sent!';
    btn.style.background = "#2a4a38";
    btn.style.opacity = "1";
    setTimeout(() => {
      btn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> Send Message';
      btn.style.background = "";
    }, 3500);
  }, 1800);
}

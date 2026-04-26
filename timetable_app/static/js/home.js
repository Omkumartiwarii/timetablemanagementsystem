document.addEventListener("DOMContentLoaded", () => {
  /* ================= MENU ================= */
  const menuToggle = document.getElementById("menuToggle");
  const navLinks = document.getElementById("navLinks");
  const overlay = document.getElementById("overlay");

  if (menuToggle && navLinks && overlay) {
    menuToggle.addEventListener("click", () => {
      menuToggle.classList.toggle("active");
      navLinks.classList.toggle("active");
      overlay.classList.toggle("active");
    });

    overlay.addEventListener("click", () => {
      menuToggle.classList.remove("active");
      navLinks.classList.remove("active");
      overlay.classList.remove("active");
    });
  }

  /* ================= SCROLL ANIMATION ================= */
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");
      }
    });
  });

  document.querySelectorAll(".fade-up").forEach((el) => observer.observe(el));

  /* ================= CAROUSEL ================= */
  let slides = document.querySelectorAll(".slide");
  let dots = document.querySelectorAll(".dot");
  let index = 0;
  let interval;

  function showSlide(i) {
    if (slides.length === 0) return;

    slides.forEach((s) => s.classList.remove("active"));
    dots.forEach((d) => d.classList.remove("active"));

    slides[i].classList.add("active");
    if (dots[i]) dots[i].classList.add("active");

    startTyping(slides[i]);
  }

  function nextSlide() {
    index = (index + 1) % slides.length;
    showSlide(index);
  }

  window.currentSlide = function (i) {
    index = i;
    showSlide(index);
    resetAutoSlide();
  };

  function startAutoSlide() {
    interval = setInterval(nextSlide, 7000);
  }

  function resetAutoSlide() {
    clearInterval(interval);
    startAutoSlide();
  }

  /* ================= TYPING EFFECT ================= */
  function startTyping(slide) {
    let textElement = slide.querySelector(".typing");
    if (!textElement) return;

    let fullText = textElement.getAttribute("data-text");
    let i = 0;

    // prevent duplicate typing
    textElement.innerHTML = "";

    function type() {
      if (i < fullText.length) {
        textElement.innerHTML += fullText.charAt(i);
        i++;
        setTimeout(type, 100); // faster + smoother
      }
    }

    type();
  }

  // INIT
  showSlide(index);
  startAutoSlide();
});

document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".slide");
  const dots = document.querySelectorAll(".dot");
  const carousel = document.querySelector(".carousel");

  let index = 0;
  let interval;

  function showSlide(i) {
    slides.forEach((s, idx) => {
      s.classList.toggle("active", idx === i);
    });

    dots.forEach((d, idx) => {
      d.classList.toggle("active", idx === i);
    });
  }

  function nextSlide() {
    index = (index + 1) % slides.length;
    showSlide(index);
  }

  function startAutoSlide() {
    interval = setInterval(nextSlide, 6000);
  }

  function stopAutoSlide() {
    clearInterval(interval);
  }

  // dots click
  window.currentSlide = (i) => {
    index = i;
    showSlide(index);
    stopAutoSlide();
    startAutoSlide();
  };

  // pause on hover
  carousel.addEventListener("mouseenter", stopAutoSlide);
  carousel.addEventListener("mouseleave", startAutoSlide);

  // init
  showSlide(index);
  startAutoSlide();
});

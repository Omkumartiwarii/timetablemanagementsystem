/* CLOCK */

function updateClock() {
  const now = new Date();

  document.getElementById("clock").textContent = now.toLocaleTimeString();

  document.getElementById("clockDate").textContent = now.toLocaleDateString(
    undefined,
    {
      weekday: "long",
      year: "numeric",
      month: "short",
      day: "numeric",
    },
  );
}

setInterval(updateClock, 1000);

updateClock();

/* GREETING */

(function () {
  const h = new Date().getHours();

  const msg =
    h < 12 ? "Good Morning" : h < 17 ? "Good Afternoon" : "Good Evening";

  document.getElementById("greeting").textContent = `${msg}, Admin 👋`;
})();

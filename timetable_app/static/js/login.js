// TAB SWITCH
function switchTab(role) {
  document.querySelectorAll(".login-form").forEach((form) => {
    form.classList.remove("active");
  });

  document.querySelectorAll(".tab-btn").forEach((btn) => {
    btn.classList.remove("active");
  });

  document.getElementById(role + "Form").classList.add("active");

  document
    .getElementById("tab" + role.charAt(0).toUpperCase() + role.slice(1))
    .classList.add("active");
}

// SHOW / HIDE PASSWORD
function togglePassword(inputId, icon) {
  const input = document.getElementById(inputId);

  if (input.type === "password") {
    input.type = "text";
    icon.textContent = "🙈";
  } else {
    input.type = "password";
    icon.textContent = "👁️";
  }
}

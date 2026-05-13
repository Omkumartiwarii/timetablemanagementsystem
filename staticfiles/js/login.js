function showAdmin() {
  document.getElementById("adminForm").style.display = "block";
  document.getElementById("studentForm").style.display = "none";
  document.getElementById("adminBtn").classList.add("active");
  document.getElementById("studentBtn").classList.remove("active");
}

function showStudent() {
  document.getElementById("adminForm").style.display = "none";
  document.getElementById("studentForm").style.display = "block";
  document.getElementById("studentBtn").classList.add("active");
  document.getElementById("adminBtn").classList.remove("active");
}

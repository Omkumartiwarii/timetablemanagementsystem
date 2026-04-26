function downloadPDF() {
  const element = document.getElementById("timetable");

  const semSelect = document.querySelector('select[name="semester"]');
  const deptSelect = document.querySelector('select[name="department"]');

  let semText = semSelect.options[semSelect.selectedIndex].text;
  let deptText = deptSelect.options[deptSelect.selectedIndex].text;

  semText = semText.replace(/\s+/g, "_");
  deptText = deptText.replace(/\s+/g, "_");

  let fileName = "timetable";

  if (deptText !== "Department") {
    fileName = deptText;
  }

  if (semText !== "Semester") {
    fileName += "_" + semText;
  }

  fileName += ".pdf";

  const opt = {
    margin: 5,
    filename: fileName,
    image: { type: "jpeg", quality: 1 },
    html2canvas: { scale: 3 },
    jsPDF: {
      unit: "mm",
      format: "a4",
      orientation: "landscape",
    },
    pagebreak: { mode: ["avoid-all", "css"] },
  };

  html2pdf().set(opt).from(element).save();
}
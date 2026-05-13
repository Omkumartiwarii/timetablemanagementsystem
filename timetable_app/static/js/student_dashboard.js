/* ═══════════════ DOWNLOAD PDF ═══════════════ */

function downloadPDF() {
  /* Hide unwanted sections while printing */
  const style = document.createElement("style");

  style.id = "print-style";

  style.innerHTML = `
  
    @media print {

      body{
        background:#ffffff !important;
        padding:0 !important;
        margin:0 !important;
      }

      .navbar,
      .filter-card,
      .footer-strip,
      .btn-download{
        display:none !important;
      }

      .main{
        padding:0 !important;
        margin:0 !important;
        max-width:100% !important;
      }

      #timetable{
        width:100% !important;
      }

      .tt-card{
        box-shadow:none !important;
        border:1px solid #ccc !important;
        margin-bottom:20px !important;
        break-inside:avoid !important;
        page-break-inside:avoid !important;
      }

      table{
        width:100% !important;
        border-collapse:collapse !important;
      }

      th, td{
        border:1px solid #ccc !important;
        padding:6px !important;
        font-size:10px !important;
        text-align:center !important;
        color:#000 !important;
        background:#fff !important;
      }

      .cell-busy{
        background:#fff !important;
      }

    }
  `;

  document.head.appendChild(style);

  /* Open Print Dialog */
  window.print();

  /* Remove temporary style after printing */
  setTimeout(() => {
    const printStyle = document.getElementById("print-style");

    if (printStyle) {
      printStyle.remove();
    }
  }, 1000);
}

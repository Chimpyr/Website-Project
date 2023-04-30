
window.jsPDF = window.jspdf.jsPDF;

function test() {
    console.log('testing456');
}


function createPDF() {
    // console.log('downloadingPDF');
    // create a new jsPDF instance
    const element = document.getElementById("bookingData");
    const opt = {
        margin: [0.5, 0.5, 0.5, 0.5],
        filename: "booking_receipt.pdf",
        image: { type: "jpeg", quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
    };
    html2pdf().set(opt).from(element).save();
  }
  



/*
Extracted from mm_report_utilities
*/
function recalculateBodyHeight() {
    document.getElementById("body-div").style.height = window.innerHeight * 0.99 - document.getElementById("header-div").offsetHeight + "px";
}
recalculateBodyHeight()
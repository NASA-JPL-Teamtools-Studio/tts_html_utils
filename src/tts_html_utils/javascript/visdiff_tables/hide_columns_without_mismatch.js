//hide_columns_without_mismatch.js
  function hideUnmatchedColumnsBySelector(selector) {
    const table = document.querySelector(selector);
    if (!table || !(table instanceof HTMLTableElement)) return;

    const rows = Array.from(table.rows);
    if (rows.length === 0) return;

    const columnCount = rows[0].cells.length;
    const keepColumn = Array(columnCount).fill(false);

    // Mark columns that contain at least one cell with 'mismatched_cell'
    rows.forEach(row => {
      Array.from(row.cells).forEach((cell, index) => {
        if (cell.classList.contains("mismatched_cell")) {
          keepColumn[index] = true;
        }
      });
    });

    // Hide columns that have no 'mismatched_cell'
    rows.forEach(row => {
      Array.from(row.cells).forEach((cell, index) => {
        if (!keepColumn[index]) {
          cell.style.display = "none";
        }
      });
    });
  }

  // Example usage
  document.addEventListener("DOMContentLoaded", function () {
    hideUnmatchedColumnsBySelector("#{{ left_table_id }}");
    hideUnmatchedColumnsBySelector("#{{ right_table_id }}");
  });
//static_html_filter_table.js
document.addEventListener("DOMContentLoaded", function () {
    const tableId = "{{ table_id }}";
    const table = document.getElementById(tableId);
    if (!table) return; // Exit if table not found
    
    const filterInputs = table.querySelectorAll('.filter-input');
    const headers = table.querySelectorAll('thead tr.header th');

    // Debounce utility to limit filter frequency
    function debounce(func, delay) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }

    // Pre-calculate column index map
    function getColumnIndexMap() {
        const map = {};
        headers.forEach((header, index) => {
            const input = header.querySelector('input');
            if (input) {
                const column = input.getAttribute('data-column');
                if (column) {
                    map[column] = index;
                }
            }
        });
        return map;
    }

    function filterTable() {
        const rows = table.querySelectorAll('tbody > tr');
        const columnIndexMap = getColumnIndexMap();

        rows.forEach(row => {
            if (!row.id.endsWith('-details')) {
                let showRow = true;

                filterInputs.forEach(input => {
                    const column = input.getAttribute('data-column');
                    const filterValue = input.value.toLowerCase();
                    const cellIndex = columnIndexMap[column];
                    const cell = row.cells[cellIndex];
                    const cellValue = cell ? (cell.textContent || '').toLowerCase() : '';

                    if (filterValue && !cellValue.includes(filterValue)) {
                        showRow = false;
                    }
                });

                const desiredDisplay = showRow ? 'table-row' : 'none';
                if (row.style.display !== desiredDisplay) {
                    row.style.display = desiredDisplay;
                }

                const detailsRow = document.getElementById(row.id + '-details');
                if (detailsRow && detailsRow.style.display !== desiredDisplay) {
                    detailsRow.style.display = desiredDisplay;
                }
            }
        });
    }

    const debouncedFilter = debounce(filterTable, 200);

    filterInputs.forEach(input => {
        input.addEventListener('input', debouncedFilter);
    });
});

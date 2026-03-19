//static_html_table_sort.js
document.addEventListener("DOMContentLoaded", function () {
    const tableId = "{{ table_id }}";
    const sortState = {};
    let pressCount = 0;

    // Get all the .*-sort ID elements within this specific table
    const table = document.getElementById(tableId);
    if (!table) return; // Exit if table not found
    
    const sortElements = table.querySelectorAll('[id$="-sort"]');

    // Add event listeners to sort elements
    sortElements.forEach(element => {
        element.addEventListener('click', onSortClick);
    });

    // Function to handle sorting click event
    function onSortClick(event) {
        const sortId = event.target.id; // Get the ID of the clicked element
        const column = getColumnIndexFromSortId(sortId);

        pressCount++;

        // Initialize the press count for this column if it doesn't exist
        if (!sortState[column]) {
            sortState[column] = { direction: 'ascending', pressCount: pressCount }; // First press, ascending
        } else {
            sortState[column].pressCount = pressCount;

            // Toggle the direction based on the press count
            if (sortState[column].direction === null) {
                sortState[column].direction = 'ascending'; // First press sets ascending
            } else if (sortState[column].direction === 'ascending') {
                sortState[column].direction = 'descending'; // Second press sets descending
            } else if (sortState[column].direction === 'descending') {
                sortState[column].direction = null; // Reset if third press
            }
        }

        // Call sorting function with the updated sort state
        sortTable();
    }

    // Function to sort the table based on sortState
    function sortTable() {
        // Sort the columns by pressCount (number of times clicked)
        const sortedEntries = Object.entries(sortState).sort((a, b) => b[1].pressCount - a[1].pressCount);

        // Filter out columns that have a 'null' direction
        const filteredEntries = sortedEntries.filter(entry => entry[1].direction !== null);

        // Extract sorted keys (column indices) and directions
        const sortColumns = filteredEntries.map(entry => entry[0]); // Column indices
        const sortDirections = filteredEntries.map(entry => entry[1].direction); // Sort directions (ascending, descending)

        // Get all rows of the table
        const primary_rows = Array.from(table.querySelectorAll('tbody > tr'))
            .filter(row => !row.id.includes('-details')); // Only include rows without '-details'

        // Sort rows based on the columns in sortColumns
        primary_rows.sort((rowA, rowB) => {
            let comparison = 0;
            for (let i = 0; i < sortColumns.length; i++) {
                const columnIndex = sortColumns[i];
                const direction = sortDirections[i];

                const cellA = rowA.cells[columnIndex].textContent.trim();
                const cellB = rowB.cells[columnIndex].textContent.trim();

                // Compare the values of the column
                if (cellA < cellB) {
                    comparison = -1;
                } else if (cellA > cellB) {
                    comparison = 1;
                }

                // Reverse the comparison if the direction is descending
                if (direction === 'descending') {
                    comparison = -comparison;
                }

                // If comparison is not 0, break the loop, no need to check further columns
                if (comparison !== 0) {
                    break;
                }
            }

            return comparison;
        });

        // Re-append the sorted rows to the table
        const tbody = table.querySelector('tbody');
        primary_rows.forEach(row => {
            tbody.appendChild(row); // Append the sorted main row
            
            // Check if the corresponding -details row exists
            const detailsRow = document.getElementById(`${row.id}-details`);
            if (detailsRow) {
                tbody.appendChild(detailsRow); // Append the related -details row after the main row
            }
        });

    }

    // Helper function to dynamically map sort ID to the corresponding column index
    function getColumnIndexFromSortId(sortId) {
        const headers = table.querySelectorAll('thead > tr.header > th');
        let columnIndex = null;

        // Loop through all header cells and match the ID of the sort element to the corresponding column
        headers.forEach((header, index) => {
            // Find the sort elements inside the header and match their IDs
            const sortDiv = header.querySelector('div[id$="-sort"]');
            if (sortDiv && sortDiv.id === sortId) {
                columnIndex = index;
            }
        });

        return columnIndex;
    }
});
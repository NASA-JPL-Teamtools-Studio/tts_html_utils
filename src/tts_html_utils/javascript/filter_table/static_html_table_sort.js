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
        const sortId = event.currentTarget.id; // Get the ID of the element with the listener
        const column = getColumnIndexFromSortId(sortId);
        
        console.log(`Sort clicked: sortId=${sortId}, columnIndex=${column}`);

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

        // Get all rows of the table (only direct children of tbody, not nested table rows)
        const tbody = table.querySelector('tbody');
        const primary_rows = Array.from(tbody.querySelectorAll(':scope > tr'))
            .filter(row => !row.id.includes('-details')); // Only include rows without '-details'

        // Store detail rows with their parent row IDs
        const detailRowMap = {};
        primary_rows.forEach(row => {
            const detailsRow = document.getElementById(`${row.id}-details`);
            if (detailsRow) {
                detailRowMap[row.id] = detailsRow;
                // Remove detail row from DOM temporarily
                detailsRow.remove();
            }
        });

        // Sort rows based on the columns in sortColumns
        primary_rows.sort((rowA, rowB) => {
            let comparison = 0;
            for (let i = 0; i < sortColumns.length; i++) {
                const columnIndex = sortColumns[i];
                const direction = sortDirections[i];

                // Debug: log cell counts
                if (i === 0) {
                    console.log(`Sorting: rowA has ${rowA.cells.length} cells, rowB has ${rowB.cells.length} cells, trying to access index ${columnIndex}`);
                }

                // Validate cells exist
                if (!rowA.cells[columnIndex] || !rowB.cells[columnIndex]) {
                    console.error(`Missing cell at index ${columnIndex}. RowA cells: ${rowA.cells.length}, RowB cells: ${rowB.cells.length}`);
                    continue;
                }

                const cellA = rowA.cells[columnIndex].textContent.trim();
                const cellB = rowB.cells[columnIndex].textContent.trim();

                // Try to parse as numbers for numeric comparison
                const numA = parseFloat(cellA);
                const numB = parseFloat(cellB);
                
                // If both are valid numbers, compare numerically
                if (!isNaN(numA) && !isNaN(numB)) {
                    comparison = numA - numB;
                } else {
                    // Otherwise compare as strings (case-insensitive)
                    const strA = cellA.toLowerCase();
                    const strB = cellB.toLowerCase();
                    if (strA < strB) {
                        comparison = -1;
                    } else if (strA > strB) {
                        comparison = 1;
                    }
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

        // Clear tbody and re-append sorted rows with their detail rows
        tbody.innerHTML = '';
        primary_rows.forEach(row => {
            tbody.appendChild(row); // Append the sorted main row
            
            // Re-insert the detail row if it exists
            if (detailRowMap[row.id]) {
                tbody.appendChild(detailRowMap[row.id]);
            }
        });

    }

    // Helper function to dynamically map sort ID to the corresponding column index
    function getColumnIndexFromSortId(sortId) {
        const headers = table.querySelectorAll('thead > tr.header > th');
        let columnIndex = null;

        console.log(`Looking for sortId: ${sortId} among ${headers.length} headers`);

        // Loop through all header cells and match the ID of the sort element to the corresponding column
        headers.forEach((header, index) => {
            // Find the sort elements inside the header and match their IDs
            const sortDiv = header.querySelector('div[id$="-sort"]');
            console.log(`  Header ${index}: sortDiv=${sortDiv ? sortDiv.id : 'none'}`);
            if (sortDiv && sortDiv.id === sortId) {
                columnIndex = index;
                console.log(`  -> MATCH at index ${index}`);
            }
        });

        console.log(`Final columnIndex: ${columnIndex}`);
        return columnIndex;
    }
});
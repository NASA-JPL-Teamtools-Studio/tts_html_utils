
Requirements
=================

This page was generated automatically during the Sphinx build process.

**Build Timestamp:** 2026-05-11 16:06:46

.. raw:: html

    <script>//show_hide_details.js
    document.addEventListener("DOMContentLoaded", function () {
        const rows = document.querySelectorAll('table[id="power-table-abe608e1-c12d-4bf0-9305-8c669673a40e"] > tbody > tr');

        rows.forEach(row => {
            if (!row.id.endsWith('-details')) {
                row.addEventListener('click', function (event) {
                    // Prevent toggle if the click is on a link or inside a link
                    if (event.target.closest('a')) {
                        return;
                    }

                    const detailsRow = document.getElementById(row.id + '-details');
                    if (detailsRow) {
                        const detailsCell = detailsRow.querySelector('td');
                        if (detailsCell) {
                            const isHidden = detailsCell.style.display === 'none';
                            detailsCell.style.display = isHidden ? '' : 'none';
                        }
                    }
                });
            }
        });
    });</script>
    <script>//static_html_filter_table.js
    document.addEventListener("DOMContentLoaded", function () {
        const tableId = "power-table-abe608e1-c12d-4bf0-9305-8c669673a40e";
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
    });</script>
    <script>//static_html_table_sort.js
    document.addEventListener("DOMContentLoaded", function () {
        const tableId = "power-table-abe608e1-c12d-4bf0-9305-8c669673a40e";
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
    });</script>
    <style>/* Read the Docs Modern Table Theme 
       Tailored for tts-html-utils requirements tables
    */

    /* Table Container & Base */
    .power-table {
        width: 100%;
        border-collapse: collapse;
        margin: 24px 0;
        font-family: "Lato", "proxima-nova", "Helvetica Neue", Arial, sans-serif;
        font-size: 14px;
        color: #404040;
        border: 1px solid #e1e4e5 !important;
        background-color: #fff;
        table-layout: auto; /* Allows columns to shrink/grow based on content */
    }

    /* Header Styling */
    .power-table thead tr.header {
        background: #f3f6f6;
    }

    .power-table th {
        font-weight: bold;
        color: #2980b9; 
        padding: 12px;
        border: 1px solid #e1e4e5;
        text-align: left;
        vertical-align: top;
    }

    /* --- Specific Column Width Control --- */

    /* Level and ID: Minimal width */
    .power-table th:nth-child(1), .power-table td:nth-child(1),
    .power-table th:nth-child(2), .power-table td:nth-child(2),
    .power-table th:nth-child(5), .power-table td:nth-child(5) {
        width: 50px;
    }

    /* Description & Rationale (4th & 5th): Flexible / Wide */
    .power-table th:nth-child(3), .power-table td:nth-child(3),
    .power-table th:nth-child(4), .power-table td:nth-child(4) {
        min-width: 200px;
    }

    /* --- Header Elements (Sort & Filter) --- */

    .power-table th > div[id$="-sort"] {
        display: block;
        margin-bottom: 10px;
        cursor: pointer;
        font-size: 13px;
        position: relative;
        padding-right: 18px;
        white-space: nowrap;
    }

    .power-table th > div[id$="-sort"]::after {
        content: "↕";
        position: absolute;
        right: 0;
        color: #adadad;
        font-size: 11px;
    }

    .filter-input {
        display: block;
        width: 100%;
        height: 30px;
        padding: 4px 8px;
        border: 1px solid #d1d4d5;
        border-radius: 3px;
        font-size: 12px;
        font-family: inherit;
        box-sizing: border-box; 
        background-color: #ffffff;
    }

    .filter-input:focus {
        border-color: #2980b9;
        outline: none;
        box-shadow: 0 0 4px rgba(41, 128, 185, 0.2);
    }

    /* --- Body Rows --- */

    .power-table tbody tr {
        border-bottom: 1px solid #e1e4e5;
        transition: background-color 0.1s ease;
    }

    .power-table td {
        padding: 10px 12px;
        line-height: 1.6;
        vertical-align: top;
        border: 1px solid #e1e4e5;
    }

    /* Alternating Row Color (Striping) */
    .power-table.alternating tbody tr.prime_row:nth-of-type(4n+1) {
        background-color: #ffffff;
    }

    .power-table.alternating tbody tr.prime_row:nth-of-type(4n+3) {
        background-color: #fcfcfc;
    }

    .power-table tbody tr.prime_row:hover {
        background-color: #f5f7f8 !important;
        cursor: pointer;
    }

    /* Details Row (Hidden Content) */
    .detail_row td {
        background-color: #fbfbfb;
        padding: 0;
        border-top: none;
    }

    /* Sticky Header Logic */
    .sticky-header thead {
        position: sticky;
        top: 0;
        z-index: 10;
        background: #f3f6f6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }</style>

    <table id="power-table-abe608e1-c12d-4bf0-9305-8c669673a40e" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""><div id="level-sort">Level</div><input type="text" id="level-filter" class="filter-input" data-column="level"></th>
        
                <th  class=""><div id="id-sort">ID</div><input type="text" id="id-filter" class="filter-input" data-column="id"></th>
        
                <th  class=""><div id="name-sort">Name</div><input type="text" id="name-filter" class="filter-input" data-column="name"></th>
        
                <th  class=""><div id="v&v-method-sort">V&V Method</div><input type="text" id="v&v-method-filter" class="filter-input" data-column="v&v-method"></th>
        
                <th  class=""><div id="status-sort">Status</div><input type="text" id="status-filter" class="filter-input" data-column="status"></th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="ee93af15-3388-46c7-bbc1-983564bd9186" class="prime_row"><td>1</td><td>R1</td><td>Pythonic Interface for Web-Agnostic Developers</td><td>Hierarchy</td><td> </td></tr>
    
            <tr id="ee93af15-3388-46c7-bbc1-983564bd9186-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-ba21c0f1-9382-4340-9514-3db79d063ac6" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="e36721c4-9a91-4e6f-aff3-0a55f64139cb" class="prime_row"><td>Description</td><td>The library provide an object-oriented framework that represents the HTML DOM as a tree of Python objects, allowing developers to build complex structures using native Python patterns.</td></tr>
    
            <tr id="e36721c4-9a91-4e6f-aff3-0a55f64139cb-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="c8355061-a75d-4f75-9f1b-99c7f94fc924" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>Teamtool developers are typically not web developers, but still need to have basic web design capabilities. To limit the diversity of the tech stack needed for competency in TTS, the studio has chosen to use Python as much as possible. Using an object oriented style allows users to avoid writing large f-strings of inscrutable HTML markup.</td></tr>
    
            <tr id="c8355061-a75d-4f75-9f1b-99c7f94fc924-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="fabd593f-7dbd-434d-96f0-de790c26892d" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="fabd593f-7dbd-434d-96f0-de790c26892d-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="692a216f-c4b6-4e78-b1d7-086195eda5db" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="692a216f-c4b6-4e78-b1d7-086195eda5db-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="f35130ce-1c49-49db-9615-00de5d502ef2" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="f35130ce-1c49-49db-9615-00de5d502ef2-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="28c4cda3-86b8-4462-9001-e7b5256594bf" class="prime_row" style="background-color: #EEEEEE;"><td>2</td><td>R1.1</td><td>Automated Asset Injection and Dependency Resolution</td><td>Inspection</td><td> </td></tr>
    
            <tr id="28c4cda3-86b8-4462-9001-e7b5256594bf-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-3a01bd42-922d-4949-be5b-31165bc94bb6" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="813e5423-c4cb-4dad-b7e7-00ec95ddb471" class="prime_row"><td>Description</td><td>The library shall automatically identify, aggregate, and deduplicate all CSS and JavaScript resources required by the components within a document, injecting them into the `<head>` during the compilation phase.</td></tr>
    
            <tr id="813e5423-c4cb-4dad-b7e7-00ec95ddb471-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="6591dc36-4a96-441f-8bc9-cc824f874a2a" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td> </td></tr>
    
            <tr id="6591dc36-4a96-441f-8bc9-cc824f874a2a-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="b66e75a0-81f0-4597-8936-1bee5f815bdc" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="b66e75a0-81f0-4597-8936-1bee5f815bdc-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="6a40911f-f1d0-46c2-9e8a-1e863dc4549d" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="6a40911f-f1d0-46c2-9e8a-1e863dc4549d-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="0b1c8022-3d2d-4e87-ba7f-86e815932e6c" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="0b1c8022-3d2d-4e87-ba7f-86e815932e6c-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="53b0a4fa-dd0e-4d2f-a804-de8a12347dde" class="prime_row"><td>2</td><td>R1.2</td><td>Extensible Widget and UI Library</td><td>Hierarchy</td><td> </td></tr>
    
            <tr id="53b0a4fa-dd0e-4d2f-a804-de8a12347dde-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-45d94460-5bea-473c-87f5-c2177a167eb0" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="2b87088e-ceec-4100-b304-24209f8e0792" class="prime_row"><td>Description</td><td>The library shall include classes for defining all common HTML tags that is extensible to other more complex entities.</td></tr>
    
            <tr id="2b87088e-ceec-4100-b304-24209f8e0792-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="385889f4-e978-41c3-9eae-2686eaac13c5" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>Users should have all of the HTML features they expect (e.g. Div, Headers, Lists, Tables) and an easy way to build out more complex features that are commonly repeated on many projects (e.g. plots, filter tables, gantt charts)</td></tr>
    
            <tr id="385889f4-e978-41c3-9eae-2686eaac13c5-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="89917a01-9331-4288-912b-bf14510768d7" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="89917a01-9331-4288-912b-bf14510768d7-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="83298523-919c-4ee5-90ad-a3946f8c903f" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="83298523-919c-4ee5-90ad-a3946f8c903f-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="2b029433-85ce-4794-ae3a-42588441cc3d" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="2b029433-85ce-4794-ae3a-42588441cc3d-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="5875fa30-9653-47f1-8867-ec1620c20b98" class="prime_row" style="background-color: #EEEEEE;"><td>3</td><td>R1.2.1</td><td>Flexbox Class</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="5875fa30-9653-47f1-8867-ec1620c20b98-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-4a29d21f-784a-498b-8ca8-a5cab0e9f4e6" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="aa6d739b-42b7-488e-9cc9-521859c2a701" class="prime_row"><td>Description</td><td>The library shall include Flexbox classes</td></tr>
    
            <tr id="aa6d739b-42b7-488e-9cc9-521859c2a701-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="fb8d1a45-c78c-4149-a9fd-fd52b8703b3d" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td> </td></tr>
    
            <tr id="fb8d1a45-c78c-4149-a9fd-fd52b8703b3d-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="5273deb7-1ffa-4d5d-b835-df348d725a3d" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="5273deb7-1ffa-4d5d-b835-df348d725a3d-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="5961e535-3d8f-4291-b606-1b80fe7eebe4" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="5961e535-3d8f-4291-b606-1b80fe7eebe4-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="cefce373-6666-4585-be0b-1581e6ed9d62" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="cefce373-6666-4585-be0b-1581e6ed9d62-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="d892c339-d72c-4adb-87ad-bd1fc164c253" class="prime_row"><td>3</td><td>R1.2.2</td><td>List Classes</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="d892c339-d72c-4adb-87ad-bd1fc164c253-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-4e59e16a-f28b-405c-8cd7-894a4036f646" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="68475cf4-fb42-4740-939d-1e9c422fb9f9" class="prime_row"><td>Description</td><td>The library shall include classes for lists</td></tr>
    
            <tr id="68475cf4-fb42-4740-939d-1e9c422fb9f9-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="7888a2f5-991e-451e-b127-704e3ff6be74" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>ol, ul, li</td></tr>
    
            <tr id="7888a2f5-991e-451e-b127-704e3ff6be74-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="da9056c3-ecb9-4497-b8c1-b2f20224adee" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="da9056c3-ecb9-4497-b8c1-b2f20224adee-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="bbebde9c-cc56-4cb3-84e8-8e46cc06e608" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="bbebde9c-cc56-4cb3-84e8-8e46cc06e608-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="52006966-3e79-407b-887f-a7981b0e79d9" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="52006966-3e79-407b-887f-a7981b0e79d9-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="98776635-e6f6-4f32-a5f5-3486f8f61237" class="prime_row" style="background-color: #EEEEEE;"><td>3</td><td>R1.2.3</td><td>Structural Classes</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="98776635-e6f6-4f32-a5f5-3486f8f61237-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-31821067-41fa-412d-aa20-f6754bcc278e" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="fef6c546-4c37-474d-a824-511e53c90c59" class="prime_row"><td>Description</td><td>The library shall include classes for commons structural elements</td></tr>
    
            <tr id="fef6c546-4c37-474d-a824-511e53c90c59-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="08e08f8b-dd7d-4dcd-bdd7-c8b51e5c7286" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>HTML, head, body, header, footer, style, script, title, Div, HR, BR, Anchor Tags, Buttons, H1, H2, H3, etc.</td></tr>
    
            <tr id="08e08f8b-dd7d-4dcd-bdd7-c8b51e5c7286-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="ef850547-8a31-405f-bd27-b3a445588bcc" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="ef850547-8a31-405f-bd27-b3a445588bcc-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="4dacd573-23a4-4980-8347-b61bacf724cd" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="4dacd573-23a4-4980-8347-b61bacf724cd-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="8cadc982-eeba-4be4-b689-8205a259edfa" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="8cadc982-eeba-4be4-b689-8205a259edfa-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="56f44080-de45-45b9-b923-710aa4358943" class="prime_row"><td>3</td><td>R1.2.4</td><td>Plot Classes</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="56f44080-de45-45b9-b923-710aa4358943-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-3ce38a5b-4de2-4873-9734-be90800ef0f4" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="450cf2fe-f5a0-47c2-afb4-1901bb7719c4" class="prime_row"><td>Description</td><td>The library shall include classes for including plots of common types</td></tr>
    
            <tr id="450cf2fe-f5a0-47c2-afb4-1901bb7719c4-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="d6ee89ba-c913-4cb1-a9a5-bd0a29e1f8d7" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>This requirement is an active area of development as we decide our standards, but for now this really just means Plotly. We are also considering D3, but have not yet made progress in that direction yet.</td></tr>
    
            <tr id="d6ee89ba-c913-4cb1-a9a5-bd0a29e1f8d7-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="d0687116-37b2-4a70-bd11-209cf4f2e1cd" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="d0687116-37b2-4a70-bd11-209cf4f2e1cd-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="06335ff6-01fa-4577-bb2a-67e094300226" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="06335ff6-01fa-4577-bb2a-67e094300226-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="7b931532-29b1-4c5e-9d89-0ea7bda2b594" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="7b931532-29b1-4c5e-9d89-0ea7bda2b594-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="c6ac4483-147d-4ab3-8fe8-0595f1d9eb82" class="prime_row" style="background-color: #EEEEEE;"><td>3</td><td>R1.2.5</td><td>Table Classes</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="c6ac4483-147d-4ab3-8fe8-0595f1d9eb82-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-a96712ae-edaf-4378-a7f1-b1e7ad452c4e" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="0a77582a-1f85-45d3-936a-1b525b55b10f" class="prime_row"><td>Description</td><td>The library shall include classes for common table structures.</td></tr>
    
            <tr id="0a77582a-1f85-45d3-936a-1b525b55b10f-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="6353390f-8a1c-4ee3-8b61-a4bca8738e56" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>This one needs some children </td></tr>
    
            <tr id="6353390f-8a1c-4ee3-8b61-a4bca8738e56-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="ca0780b6-05fd-4d6f-91de-b22e97202e7a" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="ca0780b6-05fd-4d6f-91de-b22e97202e7a-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="f0dd3943-24a2-4e9a-976a-678e738c091d" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="f0dd3943-24a2-4e9a-976a-678e738c091d-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="f6d4591e-ca21-4f95-9449-389a1c6d5833" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="f6d4591e-ca21-4f95-9449-389a1c6d5833-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="4a2ccda6-cd70-4e74-a476-d74fb1046032" class="prime_row"><td>2</td><td>R1.3</td><td>Common Interactive UI Widgets</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="4a2ccda6-cd70-4e74-a476-d74fb1046032-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-34a91d07-3d6c-4f84-830b-af764e6ece8e" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="60044a6f-5275-4ab7-a2fc-1a1d9320ed79" class="prime_row"><td>Description</td><td>The library shall include interactive widgets common at JPL</td></tr>
    
            <tr id="60044a6f-5275-4ab7-a2fc-1a1d9320ed79-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="2dfac24c-d3b4-456d-a9a7-d58bb986dd29" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>See children for explanation of what we consider to be "common"</td></tr>
    
            <tr id="2dfac24c-d3b4-456d-a9a7-d58bb986dd29-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="3639b3ce-dc5f-4af7-adec-b09eb59f8c07" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="3639b3ce-dc5f-4af7-adec-b09eb59f8c07-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="03bec5ef-0056-44c9-87e1-320989ca1932" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="03bec5ef-0056-44c9-87e1-320989ca1932-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="5e1cd97e-cccb-4ef0-8724-ab00b89f39dd" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="5e1cd97e-cccb-4ef0-8724-ab00b89f39dd-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="bc313d44-4c02-4705-ac88-4fef9b5a24de" class="prime_row" style="background-color: #EEEEEE;"><td>3</td><td>R1.3.0</td><td>Filter Table</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="bc313d44-4c02-4705-ac88-4fef9b5a24de-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-41c08a60-cc41-40f3-888a-166ef77eb8c9" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="137027dd-c257-46a0-9f86-d3ddccce4c67" class="prime_row"><td>Description</td><td>The library shall include a common widget for creating tables that are sortable and filterable.</td></tr>
    
            <tr id="137027dd-c257-46a0-9f86-d3ddccce4c67-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="2ad20fc7-6edd-446c-b429-9efa08ef80f6" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>The same table can often represent many different views in one entity. Filtering and sorting is a key way to let users implment those views themselves with minimal input from the developer.</td></tr>
    
            <tr id="2ad20fc7-6edd-446c-b429-9efa08ef80f6-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="1e1c1cf8-024b-4ac5-9684-b92e29b1fbcd" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="1e1c1cf8-024b-4ac5-9684-b92e29b1fbcd-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="17b78d31-0ea2-4103-a749-895d4bd7743a" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="17b78d31-0ea2-4103-a749-895d4bd7743a-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="23ac690b-a21a-4c96-8aa9-ff87bd862a1a" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="23ac690b-a21a-4c96-8aa9-ff87bd862a1a-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="68ac9b49-ca7d-48a5-b6a0-7302376c5812" class="prime_row"><td>3</td><td>R1.3.1</td><td>Visual Diff</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="68ac9b49-ca7d-48a5-b6a0-7302376c5812-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-5a4a2342-46dc-470a-b6aa-4878f72d7867" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="34981c41-13e5-455b-a228-faf6a254ff8a" class="prime_row"><td>Description</td><td>The library shall incldue a common widget for creating a visual difference of two similar tables.</td></tr>
    
            <tr id="34981c41-13e5-455b-a228-faf6a254ff8a-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="b161370f-7bf7-448f-9e6c-82a7ce4af658" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>Differencing two objects (last plan vs this plan, predict vs actual, etc) is essential to low risk operations</td></tr>
    
            <tr id="b161370f-7bf7-448f-9e6c-82a7ce4af658-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="f4567487-29b1-4fe8-9f11-558698bee959" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="f4567487-29b1-4fe8-9f11-558698bee959-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="6431f803-62a7-4aca-bbde-1586de747aaa" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="6431f803-62a7-4aca-bbde-1586de747aaa-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="7525bf45-871f-43b9-ad60-dd011c9131b8" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="7525bf45-871f-43b9-ad60-dd011c9131b8-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="1efaae09-9dbb-4b0c-8fba-3181c2c22ea3" class="prime_row" style="background-color: #EEEEEE;"><td>3</td><td>R1.3.2</td><td>Gantt Chart</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="1efaae09-9dbb-4b0c-8fba-3181c2c22ea3-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-d8e8769a-f32f-46bd-a421-599c143d6742" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="fa90c9b4-8941-4fab-830a-dc6e2da8e1f9" class="prime_row"><td>Description</td><td>The library shall include a common widget for creating a Gantt chart</td></tr>
    
            <tr id="fa90c9b4-8941-4fab-830a-dc6e2da8e1f9-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="1ea491de-cfc0-4863-8485-c64ca9ff5128" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>Spacecraft operations is full of timelines.</td></tr>
    
            <tr id="1ea491de-cfc0-4863-8485-c64ca9ff5128-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="d02cb636-f643-4e59-aa35-fb29c08583be" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="d02cb636-f643-4e59-aa35-fb29c08583be-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="58dc45bb-e607-4963-98e3-98da07d4dc37" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="58dc45bb-e607-4963-98e3-98da07d4dc37-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="9724f3e7-c0cd-4e23-8375-57a93bcbf461" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="9724f3e7-c0cd-4e23-8375-57a93bcbf461-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="b9c0f1b5-2fbc-4f52-9fc0-5ea138ac12a4" class="prime_row"><td>3</td><td>R1.3.3</td><td>Pane Container</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="b9c0f1b5-2fbc-4f52-9fc0-5ea138ac12a4-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-accd59a3-b6c2-4f59-bbb4-5b347be8a5b4" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="3df4af86-5010-421d-9f06-0cab51f900a6" class="prime_row"><td>Description</td><td>The library shall include a common widget to display separate panes (sub-pages) within a single report</td></tr>
    
            <tr id="3df4af86-5010-421d-9f06-0cab51f900a6-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="eb78a8cc-521b-43aa-b586-140b6f986ad4" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>Just because it's a single file doesn't meant that the information in it can be organized in a single view. This allows users to create multiple pages in the same report</td></tr>
    
            <tr id="eb78a8cc-521b-43aa-b586-140b6f986ad4-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="d082e847-a9f8-4bf5-9499-ecba27c6c92d" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="d082e847-a9f8-4bf5-9499-ecba27c6c92d-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="8e0f4d59-e3ef-4fb7-b478-cfdf7280edf1" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="8e0f4d59-e3ef-4fb7-b478-cfdf7280edf1-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="d602fa6d-53b6-4d7d-92ff-d98035e8406d" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="d602fa6d-53b6-4d7d-92ff-d98035e8406d-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="f045cae8-d0c0-47c2-b411-b5e842942617" class="prime_row" style="background-color: #EEEEEE;"><td>1</td><td>R2</td><td>Single File Reporting</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="f045cae8-d0c0-47c2-b411-b5e842942617-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-29d2f51b-a8ae-4fb9-833b-614d7bb6ab90" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="b5c6604d-b7b5-4829-a257-46acdd50af6a" class="prime_row"><td>Description</td><td>The library shall support the creation of single HTML files with commonly used user interactivity elements.</td></tr>
    
            <tr id="b5c6604d-b7b5-4829-a257-46acdd50af6a-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="28163a0f-f77b-49e8-a0b0-903cd5fadd33" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>The most common use of this library is expected to be a single-file report that is emailed, attached to a report, or stored on a file system.</td></tr>
    
            <tr id="28163a0f-f77b-49e8-a0b0-903cd5fadd33-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="0ee40e40-a890-444d-9c10-515fe652ce7a" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="0ee40e40-a890-444d-9c10-515fe652ce7a-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="d22061c1-067b-4b6d-bf4a-f3d3807d87a1" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="d22061c1-067b-4b6d-bf4a-f3d3807d87a1-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="84d25567-54b9-4675-9679-5cc2bb008ceb" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="84d25567-54b9-4675-9679-5cc2bb008ceb-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="7d3fb5e6-7dbb-46aa-85d7-4d5f9c112eea" class="prime_row"><td>2</td><td>R2.1</td><td>Indefinite Lifetime of Output Reports</td><td>Inspection</td><td> </td></tr>
    
            <tr id="7d3fb5e6-7dbb-46aa-85d7-4d5f9c112eea-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-e2df0291-2de2-4b23-ab21-45ac0ac16761" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="4207d40f-b731-4b2c-b4a1-e3ba8b1f3c5f" class="prime_row"><td>Description</td><td>The library shall build single-file reports in such a way that they can still be accessed years or decades in the future</td></tr>
    
            <tr id="4207d40f-b731-4b2c-b4a1-e3ba8b1f3c5f-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="e9837ad1-284d-40f5-9418-4ce46ebbd965" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>This is mostly about the use of JS and CSS frameworks. In cases where the inlusion of a framework causes the single-file strategy to fail (due to files being too large), developers may want to access a hosted copy of some resources on a CDN. This is generally acceptable, but opens a risk that reports will no longer be future proof.

    The one-of-a-kind work that JPL does means that every report is a precious artifact that may be used again in the future the next time we attempt to do a similar project.

    This requirement ensures that so long as web browsers and protocols remain relatively stable, these reports will still be able to be rendered in more or less the way they were when they were new.</td></tr>
    
            <tr id="e9837ad1-284d-40f5-9418-4ce46ebbd965-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="4151ff7b-6198-420c-8c1b-dba473949a47" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="4151ff7b-6198-420c-8c1b-dba473949a47-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="0a98f8d3-9762-406a-b768-ff56aeb93955" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="0a98f8d3-9762-406a-b768-ff56aeb93955-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="37795689-70cd-4f12-96b6-2359b4f76570" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="37795689-70cd-4f12-96b6-2359b4f76570-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="61aa4a63-fe31-4f6f-9b73-df22ad02ec29" class="prime_row" style="background-color: #EEEEEE;"><td>3</td><td>R2.1.1</td><td>Don't use CDNs directly</td><td>Inspection</td><td> </td></tr>
    
            <tr id="61aa4a63-fe31-4f6f-9b73-df22ad02ec29-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-7fcc6c67-a498-4522-8091-899a86027f5f" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="1ba5632d-a94a-4e40-8995-8fd8b71042c2" class="prime_row"><td>Description</td><td>The library shall mirror any required resources accessed via Content Delivery Networks.</td></tr>
    
            <tr id="1ba5632d-a94a-4e40-8995-8fd8b71042c2-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="17a7415d-4f42-4d97-ace3-54543f33b2ea" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>Referencing a file hosted on the internet that TTS does not control introduces the risk that files will disappear over time. Mirroring any dependencies internally ensures that we keep complete control over all code that makes this codebase work.</td></tr>
    
            <tr id="17a7415d-4f42-4d97-ace3-54543f33b2ea-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="b34efa07-0926-4e9c-ba53-b3143a212183" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="b34efa07-0926-4e9c-ba53-b3143a212183-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="9a7feec9-916f-4c9b-82ed-91c498d38d9a" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="9a7feec9-916f-4c9b-82ed-91c498d38d9a-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="6a47dda1-d7c5-4def-a8c2-880d2d13d6c1" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="6a47dda1-d7c5-4def-a8c2-880d2d13d6c1-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="988bae9e-439c-44f2-b189-3e8b85a4f47c" class="prime_row"><td>3</td><td>R2.1.2</td><td>Explicit Versioning of External Resources</td><td>Inspection</td><td> </td></tr>
    
            <tr id="988bae9e-439c-44f2-b189-3e8b85a4f47c-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-cd652b5a-bb31-4ab4-a1d6-ed096d9b8a89" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="0b65258f-db72-4ebf-8f42-52ca6078fc8b" class="prime_row"><td>Description</td><td>The library shall not use unversioned external files.</td></tr>
    
            <tr id="0b65258f-db72-4ebf-8f42-52ca6078fc8b-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="4122de7b-99e5-4b1c-9e67-05e9aac47b7d" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>This keeps us from using a "latest" version of a JS or CSS entitiy when building a report. This ensures that changes to the "current" version of these resources does not affect rendering of reports made on previous versions.</td></tr>
    
            <tr id="4122de7b-99e5-4b1c-9e67-05e9aac47b7d-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="aacca3d8-fa1f-4a65-be5d-9ae80a835a59" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="aacca3d8-fa1f-4a65-be5d-9ae80a835a59-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="94064b33-7138-450d-a6ef-60b90b36f71e" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="94064b33-7138-450d-a6ef-60b90b36f71e-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="386052b8-83d5-4fed-8e74-a0e0640528ca" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="386052b8-83d5-4fed-8e74-a0e0640528ca-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="ec24773e-b745-443a-bf58-16a6d5ba1010" class="prime_row" style="background-color: #EEEEEE;"><td>3</td><td>R2.1.3</td><td>Updating Mirrored versions</td><td>Inspection</td><td> </td></tr>
    
            <tr id="ec24773e-b745-443a-bf58-16a6d5ba1010-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-b5f0b5f0-2b73-4812-8244-6952bc242a72" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="9f211bed-9690-403b-9952-c33f087fc9e8" class="prime_row"><td>Description</td><td>The library shall include a mechanism to regularly update any resources accessed by reports, and the most recent versions shall be used to the maximum feasible.</td></tr>
    
            <tr id="9f211bed-9690-403b-9952-c33f087fc9e8-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="09453e79-9f18-43a0-a639-1a36db2096bc" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>Using old JS introduces the potential of vulnerabilities, and limits the ability of developers to use the common techniques being used across the industry. We should not be stuck on old versions.</td></tr>
    
            <tr id="09453e79-9f18-43a0-a639-1a36db2096bc-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="2a903507-0e24-4547-a89b-c6e09b5ce640" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="2a903507-0e24-4547-a89b-c6e09b5ce640-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="6851c31a-0c62-4d79-91d5-7a718594adf2" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="6851c31a-0c62-4d79-91d5-7a718594adf2-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="61002015-5552-4486-8754-5933a1d84939" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="61002015-5552-4486-8754-5933a1d84939-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
            <tr id="6c304065-5871-44a3-a5b2-1551d7d21ace" class="prime_row"><td>1</td><td>R3</td><td>Interoperability with other Frameworks</td><td>Demonstration</td><td> </td></tr>
    
            <tr id="6c304065-5871-44a3-a5b2-1551d7d21ace-details" class="detail_row"><td style="display: none;" colspan="100%">
    <table id="power-table-48959f11-e3d1-4b33-87a0-86cd39b9347b" class="power-table alternating sticky-header" style="text-align: left; border: 2px black solid; " >


        <thead    >
            <tr class="header">
        
                <th  class=""></th>
        
                <th  class=""> </th>
        
            </tr>
        </thead>

        <tbody id="record-list">
    
            <tr id="ab5be913-cab6-4043-982f-ec210534e08f" class="prime_row"><td>Description</td><td>The library shall support inclusion of HTML content in Jupyter notebooks, common Pyhton web frameworks, and other common reporting tools.</td></tr>
    
            <tr id="ab5be913-cab6-4043-982f-ec210534e08f-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="71b3c4a5-29dc-413e-a88f-0a42da99434e" class="prime_row" style="background-color: #EEEEEE;"><td>Rationale </td><td>Although the most typical use of this library is expected to be standalone files that are emailed or stored on file systems, some Teamtool developers will want use it in small web applications or Jupyter notebooks. This still does not mean this needs to be a full web development framework, but should provide enough capability that building simple teamtool web apps is facilitated for developers who already know this framework.

    Other common reporting tools is meant to include things like Confluence and internal JPL web-based reporting tools</td></tr>
    
            <tr id="71b3c4a5-29dc-413e-a88f-0a42da99434e-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="472a81b4-ba46-43d4-a0cc-e6c3682cad7b" class="prime_row"><td>Implementation</td><td> </td></tr>
    
            <tr id="472a81b4-ba46-43d4-a0cc-e6c3682cad7b-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="278d89c7-dcc5-4818-a941-a7d654af5685" class="prime_row" style="background-color: #EEEEEE;"><td>Testing</td><td> </td></tr>
    
            <tr id="278d89c7-dcc5-4818-a941-a7d654af5685-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
            <tr id="bff222a0-c8a6-4d87-b792-1e29cc0dceb2" class="prime_row"><td>V&V Evidence</td><td> </td></tr>
    
            <tr id="bff222a0-c8a6-4d87-b792-1e29cc0dceb2-details" class="detail_row"><td style="display: none;" colspan="100%"></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div></td></tr>
    
        </tbody>
    </table>

    <div id="pagination">
    </div>

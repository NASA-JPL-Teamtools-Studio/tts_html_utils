//django_html_filter_table.js
    const sortState = {};
    var pressCount = 0;

    document.querySelectorAll('[id$="-sort"]').forEach(element => {
        // Add a click event listener to each matching element
        element.addEventListener('click', function() {
            // Extract the part before "-sort" from the id
            const idPrefix = element.id.replace('-sort', '');
            pressCount++;
            // Initialize the press count for this column if it doesn't exist
            if (!sortState[idPrefix]) {
                sortState[idPrefix] = { direction: 'ascending', pressCount: pressCount }; // First press, ascending
            } else {
                sortState[idPrefix].pressCount = pressCount;

                // Toggle the direction based on the press count
                if (sortSta te[idPrefix].direction === null) {
                    sortState[idPrefix].direction = 'ascending'; // First press sets ascending
                } else if (sortState[idPrefix].direction === 'ascending') {
                    sortState[idPrefix].direction = 'descending'; // Second press sets descending
                } else if (sortState[idPrefix].direction === 'descending') {
                    sortState[idPrefix].direction = null; // Second press sets descending
                }
            }

            // Call your function and pass the idPrefix and sort state
            sortList();
        });
    });


    function sortList() {
        // Sort the columns by pressCount (number of times clicked)
        const sortedEntries = Object.entries(sortState).sort((a, b) => b[1].pressCount - a[1].pressCount);

        // Filter out columns that have a 'null' direction
        const filteredEntries = sortedEntries.filter(entry => entry[1].direction !== null);

        // Extract sorted keys (column names) and directions
        const sortKeys = filteredEntries.map(entry => entry[0]); // Column names (keys)
        const sortDirections = filteredEntries.map(entry => entry[1].direction); // Sort directions (ascending, descending)

        // Grab the current GET parameters from the URL
        const currentParams = new URLSearchParams(window.location.search);

        // Remove any existing sortKeys and sortDirection from the current parameters
        currentParams.delete('sortKeys');
        currentParams.delete('sortDirections');

        // Add the updated sortKeys and sortDirection to the parameters, if they exist
        if (sortKeys.length > 0) {
            currentParams.append('sortKeys', sortKeys.join(',')); // Join keys with commas
        }
        if (sortDirections.length > 0) {
            currentParams.append('sortDirections', sortDirections.join(',')); // Join directions with commas
        }

        // Example: Update the URL with the new parameters (without reloading the page)
        // You can also use `window.location.search = currentParams.toString();` to reload the page
        history.pushState(null, '', '?' + currentParams.toString());
        const url = window.location.pathname + '?' + currentParams.toString();
        fetch(url, {
          method: 'GET',
          headers: {
              'X-Requested-With': 'XMLHttpRequest',  // Indicate this is an AJAX request
          }
        })
        .then(response => response.json())
        .then(data => {
          // Update the page content dynamically with the new filtered list and pagination
          document.getElementById('record-list').innerHTML = data.html;
          document.getElementById('pagination').innerHTML = data.pagination;
        })
        .catch(error => console.error('Error updating list:', error));
     

    };

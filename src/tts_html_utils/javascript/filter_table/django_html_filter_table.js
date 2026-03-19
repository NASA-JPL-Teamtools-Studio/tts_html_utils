//django_html_filter_table.js

  document.addEventListener('DOMContentLoaded', function () {



      let debounceTimer;

      // Get all filter input elements, including date filters from the first form
      const filters = document.querySelectorAll('.filter-input, #filter-form input');

      function populateFiltersFromURL() {
          const urlParams = new URLSearchParams(window.location.search);

          filters.forEach(filter => {
              const paramValue = urlParams.get(filter.dataset.column); // Assuming the filter inputs have 'data-column' attribute
              if (paramValue) {
                  filter.value = paramValue; // Set the value of the input field from the URL parameter
              }
          });
      }

      // Populate filter values from the URL on page load
      populateFiltersFromURL();


      filters.forEach(filter => {
          // Add event listener for both 'keyup' (for text inputs) and 'change' (for date inputs)
          if (filter.type === 'date') {
              filter.addEventListener('change', function () { // 'change' event for date filter
                  updateList();
              });
          } else {
              filter.addEventListener('keyup', function () { // 'keyup' event for other filters
                  clearTimeout(debounceTimer);
                  debounceTimer = setTimeout(() => {
                      updateList();
                  }, 50);  // 100ms delay after the user stops typing
              });
          }
      });

      function updateList() {

          // Get the current page from the URL for pagination
          const page = new URLSearchParams(window.location.search).get('page') || 1;

          // Collect all filter values from the search form and date filters
          const filterParams = {};

          document.querySelectorAll('.filter-input').forEach(input => {
              if (input.value) {
                  filterParams[input.dataset.column] = input.value; // Add filter by column
              }
          });

          // Add pagination to the params
          filterParams.page = page;

          // Build the query string from the filter parameters
          const params = new URLSearchParams();
          Object.keys(filterParams).forEach(key => {
              params.append(key, filterParams[key]);
          });

          // Create the URL with the query parameters
          const url = window.location.pathname + '?' + params.toString();
          history.pushState({ path: url }, '', url);

          // Make the AJAX request
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
      }
  });
function matchTableRowHeights{{ uuid }}(tableSelectors) {
    const tables = tableSelectors
        .map(selector => document.querySelector(selector))
        .filter(table => table); // Remove nulls if any selectors don't match

    if (tables.length < 2) return; // Need at least 2 tables to match

    const allRows = tables.map(table => Array.from(table.querySelectorAll('tr')));

    const rowCount = Math.min(...allRows.map(rows => rows.length));

    // Reset all heights
    allRows.forEach(rows => {
        for (let i = 0; i < rowCount; i++) {
            rows[i].style.height = '';
        }
    });

    for (let i = 0; i < rowCount; i++) {
        const maxHeight = Math.max(...allRows.map(rows => rows[i].offsetHeight));
        allRows.forEach(rows => {
            rows[i].style.height = `${maxHeight}px`;
        });
    }
}

function setupTableSync{{ uuid }}(tableSelectors) {
    const resizeObserver = new ResizeObserver(() => {
        matchTableRowHeights{{ uuid }}(tableSelectors);
    });

    const tables = tableSelectors
        .map(selector => document.querySelector(selector))
        .filter(table => table);

    tables.forEach(table => resizeObserver.observe(table));

    // Run initially
    window.addEventListener('load', () => {
        matchTableRowHeights{{ uuid }}(tableSelectors);
    });

    // Re-run on window resize
    window.addEventListener('resize', () => {
        matchTableRowHeights{{ uuid }}(tableSelectors);
    });
}

const tableSelectors{{ uuid }} = [
    {% for table_id in table_ids %}
        '#{{ table_id }}'{% if not loop.last %}, {% endif %}
    {% endfor %}
];

setupTableSync{{ uuid }}(tableSelectors{{ uuid }});

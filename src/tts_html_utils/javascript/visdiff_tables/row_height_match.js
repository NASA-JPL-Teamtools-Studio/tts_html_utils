function setupTableSync{{ uuid }}(tableSelectors) {
    let tables = [];
    let sizes = [];
    let pending = false;

    const sizeOf = table => {
        const rect = table.getBoundingClientRect();
        return `${rect.width}x${rect.height}`;
    };

    // All writes, then all reads, then all writes. Interleaving a read and a
    // write per row forces a full-table reflow per row, which is quadratic.
    function matchTableRowHeights() {
        pending = false;
        // Hidden tables (e.g. an inactive pane) have no layout to measure; the
        // ResizeObserver re-runs this when they become visible.
        if (tables.length < 2 || tables.some(table => table.offsetParent === null)) return;

        const allRows = tables.map(table => table.rows);
        const rowCount = Math.min(...allRows.map(rows => rows.length));

        for (const rows of allRows) {
            for (let i = 0; i < rowCount; i++) rows[i].style.height = '';
        }

        const heights = new Float64Array(rowCount);
        for (const rows of allRows) {
            for (let i = 0; i < rowCount; i++) {
                heights[i] = Math.max(heights[i], rows[i].getBoundingClientRect().height);
            }
        }
        for (const rows of allRows) {
            for (let i = 0; i < rowCount; i++) rows[i].style.height = `${heights[i]}px`;
        }
        sizes = tables.map(sizeOf);
    }

    function schedule() {
        if (pending) return;
        pending = true;
        requestAnimationFrame(matchTableRowHeights);
    }

    function init() {
        tables = tableSelectors
            .map(selector => document.querySelector(selector))
            .filter(table => table);
        matchTableRowHeights();

        // Skip sizes matchTableRowHeights produced itself, so its own writes
        // don't re-trigger it. Anything else (pane shown, width change, a detail
        // row expanded) re-matches.
        const resizeObserver = new ResizeObserver(() => {
            if (tables.some((table, i) => sizeOf(table) !== sizes[i])) schedule();
        });
        tables.forEach(table => resizeObserver.observe(table));

        // Late font loads can change heights without changing width.
        window.addEventListener('load', schedule);
        window.addEventListener('resize', schedule);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}

const tableSelectors{{ uuid }} = [
    {% for table_id in table_ids %}
        '#{{ table_id }}'{% if not loop.last %}, {% endif %}
    {% endfor %}
];

setupTableSync{{ uuid }}(tableSelectors{{ uuid }});

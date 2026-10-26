document.addEventListener("DOMContentLoaded", function () {
    const tableId = "{{ table_id }}";
    const table = document.getElementById(tableId);
    if (!table) return;

    const tbody = table.querySelector("tbody");
    const pagination = document.getElementById(`${tableId}-pagination`);
    if (!tbody || !pagination) return;

    let pageSize = {{ page_size }};
    let currentPage = 1;
    let filtered = null;

    function primaryRows() {
        return Array.from(tbody.querySelectorAll(":scope > tr"))
            .filter(row => !row.id.endsWith("-details"));
    }

    function visibleRows() {
        return primaryRows().filter(row => row.style.display !== "none");
    }

    function setRowDisplay(row, display) {
        row.style.display = display;
        const detailsRow = document.getElementById(`${row.id}-details`);
        if (detailsRow) detailsRow.style.display = display;
    }

    function render() {
        const rows = filtered || visibleRows();
        const pageCount = Math.max(1, Math.ceil(rows.length / pageSize));
        currentPage = Math.min(currentPage, pageCount);
        const firstRow = (currentPage - 1) * pageSize;
        const pageRows = new Set(rows.slice(firstRow, firstRow + pageSize));

        primaryRows().forEach(row => {
            setRowDisplay(row, pageRows.has(row) ? "table-row" : "none");
        });

        pagination.replaceChildren();
        const previous = document.createElement("button");
        previous.type = "button";
        previous.textContent = "Previous";
        previous.disabled = currentPage === 1;
        previous.addEventListener("click", function () {
            currentPage -= 1;
            render();
        });

        const next = document.createElement("button");
        next.type = "button";
        next.textContent = "Next";
        next.disabled = currentPage === pageCount;
        next.addEventListener("click", function () {
            currentPage += 1;
            render();
        });

        const sizeLabel = document.createElement("label");
        sizeLabel.textContent = "Rows per page: ";
        const sizeSelect = document.createElement("select");
        [25, 50, 100, 250].forEach(size => {
            const option = document.createElement("option");
            option.value = size;
            option.textContent = size;
            option.selected = size === pageSize;
            sizeSelect.appendChild(option);
        });
        sizeSelect.addEventListener("change", function () {
            pageSize = Number(sizeSelect.value);
            currentPage = 1;
            render();
        });
        sizeLabel.appendChild(sizeSelect);

        const status = document.createElement("span");
        status.textContent = ` Page ${currentPage} of ${pageCount} (${rows.length} rows) `;
        pagination.append(previous, status, next, sizeLabel);
    }

    table.addEventListener("table:updated", function (event) {
        if (event.detail && event.detail.type === "filter") {
            filtered = primaryRows().filter(row => row.style.display !== "none");
        }
        currentPage = 1;
        render();
    });
    filtered = primaryRows();
    render();
});

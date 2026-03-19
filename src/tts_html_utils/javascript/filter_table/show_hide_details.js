//show_hide_details.js
document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll('table[id="{{ table_id }}"] > tbody > tr');

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
});

// Sortable tables for Berean Bible Bots reports.
// Clicking a column header sorts by that column; clicking again reverses.
// Uses Intl.Collator with script-detected locales so Hebrew/Aramaic and
// Greek sort in their own alphabetical order, not Unicode code-point order.
(function () {
    'use strict';

    // Return the best locale for sorting based on the Unicode scripts present
    // in a sample string.  Hebrew block covers Aramaic (same script).
    function detectLocale(sample) {
        if (/[֐-׿יִ-ﭏ]/.test(sample)) return 'he';
        if (/[Ͱ-Ͽἀ-῿]/.test(sample)) return 'el';
        return 'en';
    }

    function cellText(cell) {
        return (cell ? cell.textContent.trim() : '');
    }

    function isNumericSample(values) {
        return values.length > 0 && values.every(v => v === '' || !isNaN(v.replace(/[,%]/g, '')));
    }

    function sortTable(table, colIdx, ascending) {
        const tbody = table.querySelector('tbody');
        if (!tbody) return;
        const rows = Array.from(tbody.querySelectorAll('tr'));

        // Sample up to 10 non-empty values to characterise the column
        const samples = rows
            .map(r => cellText(r.cells[colIdx]))
            .filter(Boolean)
            .slice(0, 10);

        const numeric = isNumericSample(samples);
        const headerText = cellText(table.querySelectorAll('thead th')[colIdx]);
        const locale = detectLocale(headerText + samples.join(''));
        const collator = new Intl.Collator(locale, { sensitivity: 'base', numeric: false });

        rows.sort((a, b) => {
            const va = cellText(a.cells[colIdx]);
            const vb = cellText(b.cells[colIdx]);
            if (numeric) {
                const na = parseFloat(va.replace(/[,%]/g, '')) || 0;
                const nb = parseFloat(vb.replace(/[,%]/g, '')) || 0;
                return ascending ? na - nb : nb - na;
            }
            return ascending ? collator.compare(va, vb) : collator.compare(vb, va);
        });

        rows.forEach(r => tbody.appendChild(r));
    }

    function initSortableTable(table) {
        const headers = Array.from(table.querySelectorAll('thead th'));
        if (!headers.length) return;
        // Guard against double-initialisation on SPA navigations
        if (table.dataset.sortable) return;
        table.dataset.sortable = '1';

        headers.forEach((th, idx) => {
            th.classList.add('sortable-col');
            const ind = document.createElement('span');
            ind.className = 'sort-ind';
            ind.setAttribute('aria-hidden', 'true');
            ind.textContent = '⇅'; // ⇅
            th.appendChild(ind);

            th.addEventListener('click', function () {
                const currentDir = th.dataset.sortDir || '';
                const ascending = currentDir !== 'asc';

                // Reset every header in this table
                headers.forEach((h, i) => {
                    h.dataset.sortDir = '';
                    h.classList.remove('sort-asc', 'sort-desc');
                    const s = h.querySelector('.sort-ind');
                    if (s) s.textContent = '⇅';
                });

                th.dataset.sortDir = ascending ? 'asc' : 'desc';
                th.classList.add(ascending ? 'sort-asc' : 'sort-desc');
                const s = th.querySelector('.sort-ind');
                if (s) s.textContent = ascending ? '▲' : '▼'; // ▲ ▼

                sortTable(table, idx, ascending);
            });
        });
    }

    function initAll() {
        document.querySelectorAll('.md-typeset table').forEach(initSortableTable);
    }

    // MkDocs Material's instant navigation does not fire DOMContentLoaded on
    // subsequent pages; subscribe to its document$ observable when available.
    if (typeof document$ !== 'undefined') {
        document$.subscribe(initAll);
    } else {
        document.addEventListener('DOMContentLoaded', initAll);
    }
}());

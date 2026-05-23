// Sortable tables for Berean Bible Bots reports.
// Clicking a column header sorts by that column; clicking again reverses.
//
// Exclusions (never sorted):
//   - Any page whose URL contains "/lessons/"  (paradigm & conjugation tables)
//   - Any <table data-no-sort> in the HTML
//   - 2-column key-value tables where the second header is "Value" or "Description"
//
// Sort types (auto-detected per column):
//   - Book columns  → KJV canonical order (Genesis … Revelation)
//   - Numeric       → numeric ascending/descending
//   - Text          → Intl.Collator with script-detected locale
//                     (Hebrew/Aramaic → 'he', Greek → 'el', else 'en')
(function () {
    'use strict';

    // ── KJV canonical order lookup ────────────────────────────────────────────
    const BOOK_ORDER = (function () {
        const books = [
            // OT
            ['Gen', 'Genesis'],
            ['Exo', 'Exod', 'Exodus'],
            ['Lev', 'Leviticus'],
            ['Num', 'Numbers'],
            ['Deu', 'Deut', 'Deuteronomy'],
            ['Jos', 'Josh', 'Joshua'],
            ['Jdg', 'Judg', 'Judges'],
            ['Rut', 'Ruth'],
            ['1Sa', '1 Sam', '1 Samuel'],
            ['2Sa', '2 Sam', '2 Samuel'],
            ['1Ki', '1 Kgs', '1 Kings'],
            ['2Ki', '2 Kgs', '2 Kings'],
            ['1Ch', '1 Chr', '1 Chronicles'],
            ['2Ch', '2 Chr', '2 Chronicles'],
            ['Ezr', 'Ezra'],
            ['Neh', 'Nehemiah'],
            ['Est', 'Esth', 'Esther'],
            ['Job'],
            ['Psa', 'Ps', 'Psalms', 'Psalm'],
            ['Pro', 'Prov', 'Proverbs'],
            ['Ecc', 'Eccl', 'Ecclesiastes'],
            ['Sol', 'Song', 'Song of Solomon', 'Song of Songs'],
            ['Isa', 'Isaiah'],
            ['Jer', 'Jeremiah'],
            ['Lam', 'Lamentations'],
            ['Ezk', 'Ezek', 'Ezekiel'],
            ['Dan', 'Daniel'],
            ['Hos', 'Hosea'],
            ['Joe', 'Joel'],
            ['Amo', 'Amos'],
            ['Oba', 'Obad', 'Obadiah'],
            ['Jon', 'Jonah'],
            ['Mic', 'Micah'],
            ['Nah', 'Nahum'],
            ['Hab', 'Habakkuk'],
            ['Zep', 'Zeph', 'Zephaniah'],
            ['Hag', 'Haggai'],
            ['Zec', 'Zech', 'Zechariah'],
            ['Mal', 'Malachi'],
            // NT
            ['Mat', 'Matt', 'Matthew'],
            ['Mrk', 'Mark'],
            ['Luk', 'Luke'],
            ['Jhn', 'John'],
            ['Act', 'Acts'],
            ['Rom', 'Romans'],
            ['1Co', '1 Cor', '1 Corinthians'],
            ['2Co', '2 Cor', '2 Corinthians'],
            ['Gal', 'Galatians'],
            ['Eph', 'Ephesians'],
            ['Php', 'Phil', 'Philippians'],
            ['Col', 'Colossians'],
            ['1Th', '1 Thess', '1 Thessalonians'],
            ['2Th', '2 Thess', '2 Thessalonians'],
            ['1Ti', '1 Tim', '1 Timothy'],
            ['2Ti', '2 Tim', '2 Timothy'],
            ['Tit', 'Titus'],
            ['Phm', 'Philemon'],
            ['Heb', 'Hebrews'],
            ['Jas', 'James'],
            ['1Pe', '1 Pet', '1 Peter'],
            ['2Pe', '2 Pet', '2 Peter'],
            ['1Jn', '1 John'],
            ['2Jn', '2 John'],
            ['3Jn', '3 John'],
            ['Jud', 'Jude'],
            ['Rev', 'Revelation'],
        ];
        const map = {};
        books.forEach(function (aliases, idx) {
            aliases.forEach(function (name) { map[name.toLowerCase()] = idx; });
        });
        return map;
    }());

    // Extract leading book-name token from values like "Isa 28:10, 13" or "1 Sam 7:17".
    function bookKey(text) {
        const m = text.trim().match(/^(\d\s+\S+|\S+)/);
        return m ? m[0].toLowerCase() : text.toLowerCase();
    }

    function isBookColumn(samples) {
        if (!samples.length) return false;
        const hits = samples.filter(function (v) {
            return BOOK_ORDER[bookKey(v)] !== undefined;
        });
        return hits.length / samples.length >= 0.6;
    }

    function bookRank(text) {
        const rank = BOOK_ORDER[bookKey(text)];
        return rank !== undefined ? rank : Infinity;
    }

    // ── Locale detection ──────────────────────────────────────────────────────
    function detectLocale(sample) {
        if (/[א-תיִ-פֿ]/.test(sample)) return 'he';
        if (/[Ͱ-Ͽἀ-῿]/.test(sample)) return 'el';
        return 'en';
    }

    // ── Helpers ───────────────────────────────────────────────────────────────
    function cellText(cell) { return cell ? cell.textContent.trim() : ''; }

    function isNumericSample(values) {
        return values.length > 0 && values.every(function (v) {
            return v === '' || !isNaN(v.replace(/[,% ]/g, ''));
        });
    }

    // A 2-column table whose second header is "Value" or "Description" is a
    // key-value glossary — row order is meaningful, don't sort it.
    function isKeyValueTable(headers) {
        if (headers.length !== 2) return false;
        const h1 = headers[1].textContent.trim().toLowerCase();
        return h1 === 'value' || h1 === 'description';
    }

    // ── Core sort ─────────────────────────────────────────────────────────────
    function sortTable(table, colIdx, ascending) {
        const tbody = table.querySelector('tbody');
        if (!tbody) return;
        const rows = Array.from(tbody.querySelectorAll('tr'));

        const samples = rows
            .map(function (r) { return cellText(r.cells[colIdx]); })
            .filter(Boolean)
            .slice(0, 10);

        const headerText = cellText(table.querySelectorAll('thead th')[colIdx]);

        let compare;
        if (isBookColumn(samples)) {
            compare = function (a, b) {
                const ra = bookRank(cellText(a.cells[colIdx]));
                const rb = bookRank(cellText(b.cells[colIdx]));
                return ascending ? ra - rb : rb - ra;
            };
        } else if (isNumericSample(samples)) {
            compare = function (a, b) {
                const na = parseFloat(cellText(a.cells[colIdx]).replace(/[,% ]/g, '')) || 0;
                const nb = parseFloat(cellText(b.cells[colIdx]).replace(/[,% ]/g, '')) || 0;
                return ascending ? na - nb : nb - na;
            };
        } else {
            // Detect locale from header + first few data cells so Hebrew/Greek
            // data under an English column header still sorts correctly.
            const locale = detectLocale(headerText + samples.join(''));
            const collator = new Intl.Collator(locale, { sensitivity: 'base', numeric: false });
            compare = function (a, b) {
                const va = cellText(a.cells[colIdx]);
                const vb = cellText(b.cells[colIdx]);
                return ascending ? collator.compare(va, vb) : collator.compare(vb, va);
            };
        }

        rows.sort(compare);
        rows.forEach(function (r) { tbody.appendChild(r); });
    }

    // ── Initialise one table ──────────────────────────────────────────────────
    function initSortableTable(table) {
        // Manual opt-out via attribute
        if (table.hasAttribute('data-no-sort')) return;

        const headers = Array.from(table.querySelectorAll('thead th'));
        if (!headers.length) return;
        if (table.dataset.sortable) return; // guard against double-init (SPA)

        // Skip key-value glossary tables
        if (isKeyValueTable(headers)) return;

        table.dataset.sortable = '1';

        headers.forEach(function (th, idx) {
            th.classList.add('sortable-col');
            const ind = document.createElement('span');
            ind.className = 'sort-ind';
            ind.setAttribute('aria-hidden', 'true');
            ind.textContent = '⇅';
            th.appendChild(ind);

            th.addEventListener('click', function () {
                const ascending = th.dataset.sortDir !== 'asc';

                headers.forEach(function (h) {
                    h.dataset.sortDir = '';
                    h.classList.remove('sort-asc', 'sort-desc');
                    const s = h.querySelector('.sort-ind');
                    if (s) s.textContent = '⇅';
                });

                th.dataset.sortDir = ascending ? 'asc' : 'desc';
                th.classList.add(ascending ? 'sort-asc' : 'sort-desc');
                const s = th.querySelector('.sort-ind');
                if (s) s.textContent = ascending ? '▲' : '▼';

                sortTable(table, idx, ascending);
            });
        });
    }

    // ── Entry point ───────────────────────────────────────────────────────────
    function initAll() {
        // Never sort tables on lesson pages — conjugation/paradigm row order
        // is grammatically meaningful and must not be rearranged.
        if (window.location.pathname.includes('/lessons/')) return;

        document.querySelectorAll('.md-typeset table').forEach(initSortableTable);
    }

    // MkDocs Material instant navigation fires document$ instead of DOMContentLoaded.
    if (typeof document$ !== 'undefined') {
        document$.subscribe(initAll);
    } else {
        document.addEventListener('DOMContentLoaded', initAll);
    }
}());

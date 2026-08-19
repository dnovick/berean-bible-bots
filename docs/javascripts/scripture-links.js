// Scripture reference auto-linker for Berean Bible Bots.
//
// On each page load:
//   1. Walks DOM text nodes inside .md-typeset and detects scripture references.
//   2. Wraps matches in <a class="scripture-ref"> pointing to the user's
//      preferred Bible resource (stored in localStorage).
//   3. Injects a small gear button into the page header that opens a picker
//      popup where users can change their preferred resource.
//
// Pages skipped: any URL containing /lessons/ (paradigm tables).
// Nodes skipped: text already inside <a>, <code>, <pre>, <script>, <style>.
(function () {
    'use strict';

    // ── Bible resource definitions ────────────────────────────────────────────

    var RESOURCES = [
        {
            id: 'step',
            label: 'STEP Bible',
            description: 'Free · Hebrew/Greek interlinear · no account needed',
            url: function (book, chapter, verse) {
                // STEP parses | as a query separator — must NOT be percent-encoded.
                // Format: version first, then reference (OSIS dot notation).
                var ref = osisBook(book) + '.' + chapter + '.' + verse;
                return 'https://www.stepbible.org/?q=version=KJV|reference=' + ref;
            }
        },
        {
            id: 'logos-desktop',
            label: 'Logos (desktop)',
            description: 'Opens Logos desktop app; will launch it if not running',
            url: function (book, chapter, verse) {
                // logosref:Bible.<Book><chapter>.<verse> is the Faithlife deep-link format.
                // Same reference pattern as ref.ly web links, different scheme.
                return 'logosref:Bible.' + osisBook(book) + chapter + '.' + verse;
            }
        },
        {
            id: 'logos-web',
            label: 'Logos (web)',
            description: 'Opens Logos in the browser — account required',
            url: function (book, chapter, verse) {
                return 'https://ref.ly/logosref/Bible.' +
                    osisBook(book) + chapter + '.' + verse;
            }
        },
        {
            id: 'biblegateway',
            label: 'Bible Gateway',
            description: 'Free · KJV · familiar interface',
            url: function (book, chapter, verse) {
                return 'https://www.biblegateway.com/passage/?search=' +
                    encodeURIComponent(book + ' ' + chapter + ':' + verse) +
                    '&version=KJV';
            }
        },
        {
            id: 'blueletter',
            label: 'Blue Letter Bible',
            description: 'Strong\'s numbers · word studies · free',
            url: function (book, chapter, verse) {
                // BLB uses lowercase 3-letter codes in the path
                return 'https://www.blueletterbible.org/kjv/' +
                    blbBook(book) + '/' + chapter + '/' + verse + '/';
            }
        },
        {
            id: 'biblehub',
            label: 'BibleHub',
            description: 'Interlinear · parallel versions · free',
            url: function (book, chapter, verse) {
                return 'https://biblehub.com/' +
                    bhBook(book) + '/' + chapter + '-' + verse + '.htm';
            }
        }
    ];

    var DEFAULT_RESOURCE = 'step';
    var STORAGE_KEY = 'bbb_scripture_resource';

    function getResourceId() {
        try { return localStorage.getItem(STORAGE_KEY) || DEFAULT_RESOURCE; }
        catch (e) { return DEFAULT_RESOURCE; }
    }

    function setResourceId(id) {
        try { localStorage.setItem(STORAGE_KEY, id); }
        catch (e) { /* private browsing — ignore */ }
    }

    function getResource(id) {
        for (var i = 0; i < RESOURCES.length; i++) {
            if (RESOURCES[i].id === id) return RESOURCES[i];
        }
        return RESOURCES[0];
    }

    // ── Book name tables ──────────────────────────────────────────────────────
    // Each entry: [canonical display name, OSIS code, BLB slug, BibleHub slug,
    //              ...aliases used in text (lowercase)]
    //
    // Format: { display, osis, blb, bh, match: [lowercase aliases] }

    var BOOKS = [
        { display: 'Gen',  osis: 'Gen',  blb: 'gen', bh: 'genesis',
          match: ['gen', 'genesis'] },
        { display: 'Exod', osis: 'Exod', blb: 'exo', bh: 'exodus',
          match: ['exod', 'exo', 'exodus'] },
        { display: 'Lev',  osis: 'Lev',  blb: 'lev', bh: 'leviticus',
          match: ['lev', 'leviticus'] },
        { display: 'Num',  osis: 'Num',  blb: 'num', bh: 'numbers',
          match: ['num', 'numbers'] },
        { display: 'Deut', osis: 'Deut', blb: 'deu', bh: 'deuteronomy',
          match: ['deut', 'deu', 'deuteronomy'] },
        { display: 'Josh', osis: 'Josh', blb: 'jos', bh: 'joshua',
          match: ['josh', 'jos', 'joshua'] },
        { display: 'Judg', osis: 'Judg', blb: 'jdg', bh: 'judges',
          match: ['judg', 'jdg', 'judges'] },
        { display: 'Ruth', osis: 'Ruth', blb: 'rut', bh: 'ruth',
          match: ['ruth', 'rut'] },
        { display: '1 Sam', osis: '1Sam', blb: '1sa', bh: '1_samuel',
          match: ['1 sam', '1sam', '1 samuel'] },
        { display: '2 Sam', osis: '2Sam', blb: '2sa', bh: '2_samuel',
          match: ['2 sam', '2sam', '2 samuel'] },
        { display: '1 Kgs', osis: '1Kgs', blb: '1ki', bh: '1_kings',
          match: ['1 kgs', '1kgs', '1 kings', '1 ki'] },
        { display: '2 Kgs', osis: '2Kgs', blb: '2ki', bh: '2_kings',
          match: ['2 kgs', '2kgs', '2 kings', '2 ki'] },
        { display: '1 Chr', osis: '1Chr', blb: '1ch', bh: '1_chronicles',
          match: ['1 chr', '1chr', '1 chronicles'] },
        { display: '2 Chr', osis: '2Chr', blb: '2ch', bh: '2_chronicles',
          match: ['2 chr', '2chr', '2 chronicles'] },
        { display: 'Ezra', osis: 'Ezra', blb: 'ezr', bh: 'ezra',
          match: ['ezra', 'ezr'] },
        { display: 'Neh',  osis: 'Neh',  blb: 'neh', bh: 'nehemiah',
          match: ['neh', 'nehemiah'] },
        { display: 'Esth', osis: 'Esth', blb: 'est', bh: 'esther',
          match: ['esth', 'est', 'esther'] },
        { display: 'Job',  osis: 'Job',  blb: 'job', bh: 'job',
          match: ['job'] },
        { display: 'Ps',   osis: 'Ps',   blb: 'psa', bh: 'psalms',
          match: ['ps', 'psa', 'psalm', 'psalms'] },
        { display: 'Prov', osis: 'Prov', blb: 'pro', bh: 'proverbs',
          match: ['prov', 'pro', 'proverbs'] },
        { display: 'Eccl', osis: 'Eccl', blb: 'ecc', bh: 'ecclesiastes',
          match: ['eccl', 'ecc', 'ecclesiastes'] },
        { display: 'Song', osis: 'Song', blb: 'sol', bh: 'songs',
          match: ['song', 'sol', 'song of solomon', 'song of songs'] },
        { display: 'Isa',  osis: 'Isa',  blb: 'isa', bh: 'isaiah',
          match: ['isa', 'isaiah'] },
        { display: 'Jer',  osis: 'Jer',  blb: 'jer', bh: 'jeremiah',
          match: ['jer', 'jeremiah'] },
        { display: 'Lam',  osis: 'Lam',  blb: 'lam', bh: 'lamentations',
          match: ['lam', 'lamentations'] },
        { display: 'Ezek', osis: 'Ezek', blb: 'ezk', bh: 'ezekiel',
          match: ['ezek', 'ezk', 'ezekiel'] },
        { display: 'Dan',  osis: 'Dan',  blb: 'dan', bh: 'daniel',
          match: ['dan', 'daniel'] },
        { display: 'Hos',  osis: 'Hos',  blb: 'hos', bh: 'hosea',
          match: ['hos', 'hosea'] },
        { display: 'Joel', osis: 'Joel', blb: 'joe', bh: 'joel',
          match: ['joel', 'joe'] },
        { display: 'Amos', osis: 'Amos', blb: 'amo', bh: 'amos',
          match: ['amos', 'amo'] },
        { display: 'Obad', osis: 'Obad', blb: 'oba', bh: 'obadiah',
          match: ['obad', 'oba', 'obadiah'] },
        { display: 'Jonah', osis: 'Jonah', blb: 'jon', bh: 'jonah',
          match: ['jonah', 'jon'] },
        { display: 'Mic',  osis: 'Mic',  blb: 'mic', bh: 'micah',
          match: ['mic', 'micah'] },
        { display: 'Nah',  osis: 'Nah',  blb: 'nah', bh: 'nahum',
          match: ['nah', 'nahum'] },
        { display: 'Hab',  osis: 'Hab',  blb: 'hab', bh: 'habakkuk',
          match: ['hab', 'habakkuk'] },
        { display: 'Zeph', osis: 'Zeph', blb: 'zep', bh: 'zephaniah',
          match: ['zeph', 'zep', 'zephaniah'] },
        { display: 'Hag',  osis: 'Hag',  blb: 'hag', bh: 'haggai',
          match: ['hag', 'haggai'] },
        { display: 'Zech', osis: 'Zech', blb: 'zec', bh: 'zechariah',
          match: ['zech', 'zec', 'zechariah'] },
        { display: 'Mal',  osis: 'Mal',  blb: 'mal', bh: 'malachi',
          match: ['mal', 'malachi'] },
        // NT
        { display: 'Matt', osis: 'Matt', blb: 'mat', bh: 'matthew',
          match: ['matt', 'mat', 'matthew'] },
        { display: 'Mark', osis: 'Mark', blb: 'mrk', bh: 'mark',
          match: ['mark', 'mrk'] },
        { display: 'Luke', osis: 'Luke', blb: 'luk', bh: 'luke',
          match: ['luke', 'luk'] },
        { display: 'John', osis: 'John', blb: 'jhn', bh: 'john',
          match: ['john', 'jhn'] },
        { display: 'Acts', osis: 'Acts', blb: 'act', bh: 'acts',
          match: ['acts', 'act'] },
        { display: 'Rom',  osis: 'Rom',  blb: 'rom', bh: 'romans',
          match: ['rom', 'romans'] },
        { display: '1 Cor', osis: '1Cor', blb: '1co', bh: '1_corinthians',
          match: ['1 cor', '1cor', '1 corinthians', '1co'] },
        { display: '2 Cor', osis: '2Cor', blb: '2co', bh: '2_corinthians',
          match: ['2 cor', '2cor', '2 corinthians', '2co'] },
        { display: 'Gal',  osis: 'Gal',  blb: 'gal', bh: 'galatians',
          match: ['gal', 'galatians'] },
        { display: 'Eph',  osis: 'Eph',  blb: 'eph', bh: 'ephesians',
          match: ['eph', 'ephesians'] },
        { display: 'Phil', osis: 'Phil', blb: 'php', bh: 'philippians',
          match: ['phil', 'php', 'philippians'] },
        { display: 'Col',  osis: 'Col',  blb: 'col', bh: 'colossians',
          match: ['col', 'colossians'] },
        { display: '1 Thess', osis: '1Thess', blb: '1th', bh: '1_thessalonians',
          match: ['1 thess', '1thess', '1 thessalonians', '1th'] },
        { display: '2 Thess', osis: '2Thess', blb: '2th', bh: '2_thessalonians',
          match: ['2 thess', '2thess', '2 thessalonians', '2th'] },
        { display: '1 Tim', osis: '1Tim', blb: '1ti', bh: '1_timothy',
          match: ['1 tim', '1tim', '1 timothy', '1ti'] },
        { display: '2 Tim', osis: '2Tim', blb: '2ti', bh: '2_timothy',
          match: ['2 tim', '2tim', '2 timothy', '2ti'] },
        { display: 'Titus', osis: 'Titus', blb: 'tit', bh: 'titus',
          match: ['titus', 'tit'] },
        { display: 'Philem', osis: 'Phlm', blb: 'phm', bh: 'philemon',
          match: ['philem', 'phlm', 'phm', 'philemon'] },
        { display: 'Heb',  osis: 'Heb',  blb: 'heb', bh: 'hebrews',
          match: ['heb', 'hebrews'] },
        { display: 'Jas',  osis: 'Jas',  blb: 'jas', bh: 'james',
          match: ['jas', 'james'] },
        { display: '1 Pet', osis: '1Pet', blb: '1pe', bh: '1_peter',
          match: ['1 pet', '1pet', '1 peter', '1pe'] },
        { display: '2 Pet', osis: '2Pet', blb: '2pe', bh: '2_peter',
          match: ['2 pet', '2pet', '2 peter', '2pe'] },
        { display: '1 John', osis: '1John', blb: '1jn', bh: '1_john',
          match: ['1 john', '1john', '1jn'] },
        { display: '2 John', osis: '2John', blb: '2jn', bh: '2_john',
          match: ['2 john', '2john', '2jn'] },
        { display: '3 John', osis: '3John', blb: '3jn', bh: '3_john',
          match: ['3 john', '3john', '3jn'] },
        { display: 'Jude', osis: 'Jude', blb: 'jud', bh: 'jude',
          match: ['jude', 'jud'] },
        { display: 'Rev',  osis: 'Rev',  blb: 'rev', bh: 'revelation',
          match: ['rev', 'revelation'] }
    ];

    // Build fast lookup: lowercase alias → book entry
    var BOOK_MAP = {};
    BOOKS.forEach(function (b) {
        b.match.forEach(function (alias) { BOOK_MAP[alias] = b; });
    });

    function lookupBook(raw) {
        return BOOK_MAP[raw.toLowerCase().trim()] || null;
    }

    function osisBook(displayName) {
        var b = lookupBook(displayName);
        return b ? b.osis : displayName;
    }

    function blbBook(displayName) {
        var b = lookupBook(displayName);
        return b ? b.blb : displayName.toLowerCase();
    }

    function bhBook(displayName) {
        var b = lookupBook(displayName);
        return b ? b.bh : displayName.toLowerCase();
    }

    // ── Scripture reference regex ─────────────────────────────────────────────
    // Matches: optional leading digit + space + book name + space + chapter:verse
    // Also handles: ranges (6:12–14 or 6:12-14), LXX suffix, verse lists (partially)
    // Group 1: full book name (may include leading "1 ", "2 ", "3 ")
    // Group 2: chapter
    // Group 3: verse (opening verse of a range)
    // Group 4: LXX suffix, if present (e.g. " LXX")

    // Build alternation from longest to shortest to avoid prefix shadowing.
    var bookAlts = Object.keys(BOOK_MAP).slice().sort(function (a, b) {
        return b.length - a.length;
    }).map(function (s) {
        // Escape regex special chars, then make trailing period optional (e.g. "Matt.")
        return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }).join('|');

    // Surround book alternation with word boundary on the right; left boundary
    // is handled by requiring the match start at a word boundary or digit prefix.
    // Capture an optional preceding boundary character in group 0 so we can
    // skip over it without a lookbehind (better compat across all browsers).
    // Group 1: boundary char (space/punct/empty), group 2: book, group 3: ch, group 4: verse
    var REF_PATTERN = new RegExp(
        '(^|[\\s(,;\\[])' +                          // group 1: boundary char or start
        '((?:[123]\\s)?(?:' + bookAlts + '))' +       // group 2: book name
        '\\s+(\\d{1,3}):(\\d{1,3})' +                // group 3: chapter, group 4: verse
        '(?:[\\u2013\\u2014-]\\d{1,3}(?::\\d{1,3})?)?' + // optional range end
        '(\\s+LXX)?',                                 // group 5: LXX annotation
        'gi'
    );

    // ── URL builders ─────────────────────────────────────────────────────────

    function buildUrl(book, chapter, verse) {
        var resource = getResource(getResourceId());
        return resource.url(book, chapter, verse);
    }

    // ── DOM walking ───────────────────────────────────────────────────────────

    var SKIP_TAGS = { A: 1, CODE: 1, PRE: 1, SCRIPT: 1, STYLE: 1,
                      BUTTON: 1, INPUT: 1, TEXTAREA: 1, SELECT: 1 };

    function shouldSkipNode(node) {
        var p = node.parentNode;
        while (p && p.nodeType === 1) {
            if (SKIP_TAGS[p.tagName]) return true;
            if (p.classList && p.classList.contains('md-typeset') === false &&
                p.tagName === 'BODY') break;
            p = p.parentNode;
        }
        return false;
    }

    function processTextNode(textNode) {
        if (shouldSkipNode(textNode)) return;
        var text = textNode.nodeValue;
        REF_PATTERN.lastIndex = 0;
        var match = REF_PATTERN.exec(text);
        if (!match) return;

        var fragment = document.createDocumentFragment();
        var lastIndex = 0;

        do {
            var boundary = match[1]; // space/punct char before the reference (may be '')
            var book = match[2];
            var chapter = match[3];
            var verse = match[4];
            var lxx = match[5] ? match[5].trim() : '';

            // Only linkify if the book name is actually in our map
            if (!lookupBook(book)) {
                REF_PATTERN.lastIndex = match.index + 1;
                match = REF_PATTERN.exec(text);
                continue;
            }

            // The match starts at the boundary char; the ref itself starts after it.
            var refStart = match.index + boundary.length;

            // Text before this match (including the boundary char — output it verbatim)
            if (refStart > lastIndex) {
                fragment.appendChild(document.createTextNode(
                    text.slice(lastIndex, refStart)
                ));
            }

            var href = buildUrl(book, chapter, verse);
            var a = document.createElement('a');
            a.href = href;
            // Custom URL schemes (logosref:, etc.) silently fail with target="_blank"
            // in Chrome; only set it for ordinary http/https links.
            if (/^https?:/i.test(href)) {
                a.target = '_blank';
                a.rel = 'noopener noreferrer';
            }
            a.className = 'scripture-ref';
            a.setAttribute('data-book', book);
            a.setAttribute('data-chapter', chapter);
            a.setAttribute('data-verse', verse);
            // match[0] includes the boundary char; strip it
            a.textContent = match[0].slice(boundary.length).trim();
            if (lxx) {
                a.setAttribute('data-lxx', '1');
            }
            fragment.appendChild(a);

            lastIndex = match.index + match[0].length;
            REF_PATTERN.lastIndex = lastIndex;
            match = REF_PATTERN.exec(text);
        } while (match);

        // Remaining text
        if (lastIndex < text.length) {
            fragment.appendChild(document.createTextNode(text.slice(lastIndex)));
        }

        textNode.parentNode.replaceChild(fragment, textNode);
    }

    function walkNode(root) {
        // Collect text nodes first to avoid live-collection issues during replacement
        var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
        var nodes = [];
        var node;
        while ((node = walker.nextNode())) { nodes.push(node); }
        nodes.forEach(processTextNode);
    }

    // ── Rewrite existing scripture-ref hrefs (after resource change) ──────────

    function rewriteLinks() {
        document.querySelectorAll('a.scripture-ref').forEach(function (a) {
            var book = a.getAttribute('data-book');
            var chapter = a.getAttribute('data-chapter');
            var verse = a.getAttribute('data-verse');
            if (book && chapter && verse) {
                var href = buildUrl(book, chapter, verse);
                a.href = href;
                if (/^https?:/i.test(href)) {
                    a.target = '_blank';
                    a.rel = 'noopener noreferrer';
                } else {
                    a.removeAttribute('target');
                    a.removeAttribute('rel');
                }
            }
        });
    }

    // ── Settings popup ────────────────────────────────────────────────────────

    function buildPopup() {
        var overlay = document.createElement('div');
        overlay.id = 'bbb-scripture-overlay';
        overlay.setAttribute('aria-modal', 'true');
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-label', 'Bible resource settings');

        var box = document.createElement('div');
        box.id = 'bbb-scripture-popup';

        var heading = document.createElement('h3');
        heading.textContent = 'Open scripture references in…';
        box.appendChild(heading);

        var current = getResourceId();

        RESOURCES.forEach(function (r) {
            var label = document.createElement('label');
            label.className = 'bbb-resource-option';

            var radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = 'bbb-resource';
            radio.value = r.id;
            if (r.id === current) radio.checked = true;

            var nameSpan = document.createElement('span');
            nameSpan.className = 'bbb-resource-name';
            nameSpan.textContent = r.label;

            var descSpan = document.createElement('span');
            descSpan.className = 'bbb-resource-desc';
            descSpan.textContent = r.description;

            label.appendChild(radio);
            label.appendChild(nameSpan);
            label.appendChild(descSpan);

            radio.addEventListener('change', function () {
                setResourceId(r.id);
                rewriteLinks();
                box.querySelectorAll('input[name="bbb-resource"]').forEach(function (inp) {
                    inp.checked = inp.value === r.id;
                });
                // Show/hide the Logos permission note
                var note = box.querySelector('.bbb-logos-note');
                if (note) note.style.display = r.id === 'logos-desktop' ? '' : 'none';
            });

            box.appendChild(label);

            // Chrome permission note — shown only for Logos desktop
            if (r.id === 'logos-desktop') {
                var note = document.createElement('p');
                note.className = 'bbb-logos-note';
                note.style.display = current === 'logos-desktop' ? '' : 'none';
                note.innerHTML =
                    'The first click may show a Chrome dialog — click “Open Logos” ' +
                    'to allow. If nothing happens, click the lock icon in the address bar, ' +
                    'choose “Site settings”, and make sure “Handlers” is set to Allow.';
                box.appendChild(note);
            }
        });

        var close = document.createElement('button');
        close.id = 'bbb-scripture-close';
        close.textContent = 'Done';
        close.addEventListener('click', hidePopup);
        box.appendChild(close);

        overlay.appendChild(box);
        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) hidePopup();
        });
        document.body.appendChild(overlay);

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') hidePopup();
        });

        return overlay;
    }

    var _popup = null;

    function showPopup() {
        if (!_popup) _popup = buildPopup();
        _popup.style.display = 'flex';
        _popup.querySelector('#bbb-scripture-close').focus();
    }

    function hidePopup() {
        if (_popup) _popup.style.display = 'none';
    }

    // ── Config button in page header ──────────────────────────────────────────
    // Injected once into .md-header__inner (the header persists across Material
    // instant navigation, so one injection covers all pages).

    function injectGearButton() {
        if (document.getElementById('bbb-scripture-gear')) return;

        var headerInner = document.querySelector('.md-header__inner');
        if (!headerInner) return;

        var btn = document.createElement('button');
        btn.id = 'bbb-scripture-gear';
        btn.className = 'bbb-scripture-gear';
        btn.title = 'Bible resource settings';
        btn.setAttribute('aria-label', 'Choose Bible resource for scripture links');
        btn.innerHTML =
            '<span class="bbb-sg-icon" aria-hidden="true">&#x1F4D6;</span>' +
            '<span class="bbb-sg-text">Config</span>';
        btn.addEventListener('click', showPopup);

        // Append at the far right of the inner header row
        headerInner.appendChild(btn);
    }

    // ── Entry point ───────────────────────────────────────────────────────────
    // Note: no custom click handler for logosref:/custom schemes. Calling
    // e.preventDefault() before window.location.href kills Chrome's user-gesture
    // context and silently suppresses protocol invocation. Native anchor behavior
    // on an <a> without target lets Chrome route the link to the OS handler.

    function init() {
        // Skip pages under /lessons/ — paradigm tables have too many false positives
        if (/\/lessons\//.test(window.location.pathname)) return;

        var content = document.querySelector('.md-typeset');
        if (!content) return;

        // Don't re-process if already done (Material instant nav)
        if (content.dataset.scriptureLinked) return;
        content.dataset.scriptureLinked = '1';

        walkNode(content);
    }

    // MkDocs Material instant navigation fires document$ on each page transition.
    // injectGearButton runs on every transition but is idempotent (the header
    // persists across instant nav, so the button is only ever inserted once).
    if (typeof document$ !== 'undefined') {
        document$.subscribe(function () {
            injectGearButton();
            // Reset flags so new page content is processed
            var content = document.querySelector('.md-typeset');
            if (content) {
                delete content.dataset.scriptureLinked;
            }
            init();
        });
    } else {
        document.addEventListener('DOMContentLoaded', function () {
            injectGearButton();
            init();
        });
    }
}());

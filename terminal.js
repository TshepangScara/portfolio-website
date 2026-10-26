// =============================================
// HERO TERMINAL — animated pytest run
// Types a command, streams test results, prints a summary.
// Sets data-state="running" | "done" on #heroTerminal (used by the test suite).
// =============================================
(function () {
    var terminal = document.getElementById('heroTerminal');
    var body = document.getElementById('terminalBody');
    var rerun = document.getElementById('terminalRerun');
    if (!terminal || !body) return;

    var COMMAND = 'pytest tests/test_candidate.py -v';

    var TESTS = [
        'test_istqb_ctfl_v4_certified',
        'test_igaming_compliance_mt_uk',
        'test_selenium_pytest_framework',
        'test_ships_ci_pipelines',
        'test_open_to_qa_roles',
    ];

    var reduceMotion = window.matchMedia &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var timers = [];
    function later(fn, ms) { timers.push(setTimeout(fn, ms)); }
    function clearTimers() { timers.forEach(clearTimeout); timers = []; }

    function line(html, cls) {
        var el = document.createElement('span');
        el.className = 'tline' + (cls ? ' ' + cls : '');
        if (html.indexOf('t-result') !== -1) el.className += ' tline--test';
        el.innerHTML = html;
        body.appendChild(el);
        return el;
    }

    function prompt() {
        return '<span class="t-prompt">$</span> ';
    }

    function pct(i) {
        return Math.round(((i + 1) / TESTS.length) * 100);
    }

    function testLine(name, i) {
        return '<span class="t-path"><span class="t-file">test_candidate.py::</span>' + name + '</span>' +
            '<span class="t-result"><span class="t-pass">PASSED</span>' +
            '<span class="t-pct">[' + String(pct(i)).padStart(3, '\u00a0') + '%]</span></span>';
    }

    function summary(seconds) {
        return '<span class="t-summary">=== ' + TESTS.length + ' passed in ' +
            seconds + 's ===</span>';
    }

    function finish() {
        line(prompt() + '<span class="t-cursor" aria-hidden="true"></span>');
        terminal.setAttribute('data-state', 'done');
        if (rerun) rerun.disabled = false;
    }

    function renderInstant() {
        body.innerHTML = '';
        line(prompt() + COMMAND);
        line('<span class="t-dim">collected ' + TESTS.length + ' items</span>');
        TESTS.forEach(function (t, i) { line(testLine(t, i)); });
        line(summary('0.42'));
        finish();
    }

    function run() {
        clearTimers();
        body.innerHTML = '';
        terminal.setAttribute('data-state', 'running');
        if (rerun) rerun.disabled = true;

        if (reduceMotion) { renderInstant(); return; }

        var cmdLine = line(prompt() + '<span class="t-typed"></span><span class="t-cursor"></span>');
        var typed = cmdLine.querySelector('.t-typed');
        var cursor = cmdLine.querySelector('.t-cursor');
        var t = 400;

        // Type the command character by character
        COMMAND.split('').forEach(function (ch) {
            t += 28 + Math.random() * 40;
            later(function () { typed.textContent += ch; }, t);
        });

        t += 350;
        later(function () {
            cursor.remove();
            line('<span class="t-dim">collected ' + TESTS.length + ' items</span>');
        }, t);

        // Stream each test result
        var start = Date.now();
        TESTS.forEach(function (name, i) {
            t += 260 + Math.random() * 260;
            later(function () { line(testLine(name, i), 'tline--in'); }, t);
        });

        t += 450;
        later(function () {
            var secs = ((Date.now() - start) / 1000 / 6).toFixed(2); // keep it snappy
            line(summary(secs), 'tline--in');
            finish();
        }, t);
    }

    if (rerun) rerun.addEventListener('click', run);

    // Start when the terminal scrolls into view (it's above the fold on desktop)
    if ('IntersectionObserver' in window) {
        var io = new IntersectionObserver(function (entries) {
            if (entries[0].isIntersecting) { io.disconnect(); run(); }
        }, { threshold: 0.3 });
        io.observe(terminal);
    } else {
        renderInstant();
    }
})();

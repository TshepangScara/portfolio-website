// =============================================
// FLOATING CODE FRAGMENTS (themed for light/dark mode)
// =============================================
(function () {
    var FRAGMENTS = [
        'const test =', 'async/await', 'driver.findElement()', 'By.id("")',
        'assert.equal()', '@Test', 'WebDriver', '.click()', '.sendKeys()',
        'expect(true)', 'describe()', 'it("should pass")', 'npm test',
        'git commit -m', 'mvn verify', 'CI/CD', '() =>', 'Promise.all()',
        'SELECT * FROM', 'WHERE id = ?', 'new WebDriver()',
        'try { }', 'catch(e) { }', 'async function()', 'ISTQB', 'xpath',
        'TestNG', 'JUnit', 'Selenium Grid', 'let result =', 'return true;',
        'null', '{}', '[]', '// TODO', 'console.log()', 'import {}',
        'export default', 'querySelector()', 'addEventListener()', '200 OK',
        'if (isPassing)', '.map()', '.filter()', '.forEach()', 'var i = 0;',
        'while (queue)', 'break;', 'continue;', '===', '!==', 'typeof',
        'document.body', 'fetch(url)', '.then(res =>', 'git push origin',
        'npm run build', 'docker run', '@BeforeTest', '@AfterSuite',
        'assert.assertTrue', 'driver.get(url)', 'implicitlyWait()',
        'By.cssSelector', 'WebElement', 'Actions actions',
        'System.out.println', 'public void test', 'mvn clean install',
    ];

    var MAX_FRAGMENTS = 38;
    var container = null;
    var spawnTimer = null;
    var active = false;
    var count = 0;

    var THEME = {
        dark:  { color: '#22c55e', opacity: 0.09 },
        light: { color: '#0066cc', opacity: 0.08 },
    };

    function rand(a, b) { return a + Math.random() * (b - a); }

    function currentTheme() {
        return document.body.classList.contains('dark-mode') ? THEME.dark : THEME.light;
    }

    function spawnFragment() {
        if (count >= MAX_FRAGMENTS) return;

        var span = document.createElement('span');
        span.textContent = FRAGMENTS[Math.floor(Math.random() * FRAGMENTS.length)];

        var dur   = rand(16, 34);
        var delay = active ? 0 : rand(-dur * 0.85, 0); // stagger on seed
        var drift = rand(-50, 50);
        var theme = currentTheme();

        span.style.cssText = [
            'position:fixed',
            'left:' + rand(0, 97) + 'vw',
            'bottom:-3rem',
            'font-size:' + rand(10, 15) + 'px',
            'animation:cfloat ' + dur.toFixed(1) + 's ' + delay.toFixed(1) + 's linear forwards',
            '--drift:' + drift.toFixed(1) + 'px',
            '--peak-opacity:' + theme.opacity,
            'pointer-events:none',
            'user-select:none',
            'white-space:nowrap',
            'color:' + theme.color,
            'font-family:"Courier New",monospace',
            'will-change:transform,opacity',
        ].join(';');

        span.addEventListener('animationend', function () {
            span.remove();
            count--;
        });

        container.appendChild(span);
        count++;
    }

    function seed() {
        for (var i = 0; i < 28; i++) spawnFragment();
    }

    function start() {
        if (active) return;
        active = true;
        container.style.display = 'block';
        seed();
        // After initial seed, mark as "live" so new spawns use delay=0
        setTimeout(function () {
            active = true; // already true, but marks seed phase done
        }, 0);
        spawnTimer = setInterval(spawnFragment, 1800);
    }

    function injectStyles() {
        var style = document.createElement('style');
        style.textContent = [
            '@keyframes cfloat {',
            '  0%   { transform: translateY(0)      translateX(0)            rotate(0deg);  opacity: 0;    }',
            '  7%   { opacity: var(--peak-opacity, 0.09); }',
            '  87%  { opacity: var(--peak-opacity, 0.09); }',
            '  100% { transform: translateY(-110vh) translateX(var(--drift)) rotate(6deg);  opacity: 0;    }',
            '}',
        ].join('\n');
        document.head.appendChild(style);
    }

    function init() {
        injectStyles();

        container = document.createElement('div');
        container.id = 'codeFragments';
        container.style.cssText = [
            'position:fixed',
            'inset:0',
            'pointer-events:none',
            'overflow:hidden',
            'z-index:0',
            'display:none',
        ].join(';');

        document.body.insertBefore(container, document.body.firstChild);

        start();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();

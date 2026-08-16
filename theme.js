// =============================================
// THEME TOGGLE
// =============================================
(function () {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    const currentTheme = localStorage.getItem('theme') || 'light';
    if (currentTheme === 'dark') {
        body.classList.add('dark-mode');
    }
    if (themeToggle) {
        updateThemeIcon(currentTheme === 'dark' ? 'light' : 'dark');
        themeToggle.addEventListener('click', function () {
            body.classList.toggle('dark-mode');
            const isDark = body.classList.contains('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            updateThemeIcon(isDark ? 'light' : 'dark');
        });
    }

    function updateThemeIcon(nextTheme) {
        const icon = themeToggle.querySelector('.theme-icon');
        if (icon) icon.textContent = nextTheme === 'dark' ? '🌙' : '☀️';
    }
})();

// =============================================
// MOBILE HAMBURGER MENU
// =============================================
(function () {
    const hamburger = document.getElementById('navHamburger');
    const navLinks = document.querySelector('.nav-links');

    if (!hamburger || !navLinks) return;

    hamburger.addEventListener('click', function () {
        const isOpen = navLinks.classList.toggle('open');
        hamburger.classList.toggle('open', isOpen);
        hamburger.setAttribute('aria-expanded', isOpen);
    });

    navLinks.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
            navLinks.classList.remove('open');
            hamburger.classList.remove('open');
            hamburger.setAttribute('aria-expanded', 'false');
        });
    });
})();

// =============================================
// BACK TO TOP
// =============================================
(function () {
    const btn = document.createElement('button');
    btn.className = 'back-to-top';
    btn.id = 'backToTop';
    btn.setAttribute('aria-label', 'Back to top');
    btn.setAttribute('title', 'Back to top');
    btn.innerHTML = '&#8593;';
    document.body.appendChild(btn);

    window.addEventListener('scroll', function () {
        btn.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });

    btn.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
})();

// =============================================
// SCROLL REVEAL
// =============================================
(function () {
    const targets = document.querySelectorAll('.section, .hero');
    if (!targets.length) return;

    targets.forEach(function (el) {
        el.classList.add('reveal');
    });

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08 });

    targets.forEach(function (el) {
        observer.observe(el);
    });
})();

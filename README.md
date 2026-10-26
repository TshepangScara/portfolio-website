# Tshepang Molete — Portfolio

[![Site tests](https://github.com/TshepangScara/portfolio-website/actions/workflows/site-tests.yml/badge.svg)](https://github.com/TshepangScara/portfolio-website/actions/workflows/site-tests.yml)

Live site: https://tshepangscara.github.io/portfolio-website/

A QA engineer's portfolio should be tested like a product, so this one is.
Every push runs an end-to-end suite with **Playwright + pytest** in GitHub Actions.

## What the suite covers

| Area | Checks |
|---|---|
| Smoke | Every page returns 200, has a title, meta description and exactly one `<h1>` |
| Stability | No console errors or uncaught JS exceptions on any page |
| Links & media | Internal links resolve, images load and have alt text, `target="_blank"` links use `rel="noopener"` |
| Behaviour | Nav routing and active state, dark-mode toggle persists across pages and reloads |
| Mobile | Hamburger menu opens/closes with correct `aria-expanded`, no horizontal scroll at 390px |
| Hero terminal | Animated run completes with 5 passed, re-run works, `prefers-reduced-motion` renders instantly |
| Accessibility | axe-core WCAG 2.1 A/AA scan on every page, in both light and dark themes |

**73 tests.** The first run of the accessibility scan found real contrast and link-styling issues on the live site, which were then fixed.

## Structure

```
tests/
├── conftest.py            # local static server, third-party request stubs, console capture
├── pages/                 # Page Object Model
│   ├── base_page.py       # shared nav, theme toggle
│   └── home_page.py       # hero terminal
├── test_pages.py          # smoke + links + images, parametrised over every page
├── test_interactions.py   # navigation, dark mode, mobile, terminal
└── test_accessibility.py  # axe-core WCAG scan, light + dark
```

## Run it locally

```bash
pip install -r requirements-test.txt
python -m playwright install chromium
pytest                       # headless
pytest --headed --slowmo 300 # watch it drive the browser
pytest --html=report/index.html --self-contained-html
```

CI uploads an HTML report and JUnit XML as a build artifact on every run, plus failure screenshots.

"""Automated accessibility checks with axe-core (WCAG 2.1 A + AA)."""
import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page

from conftest import PAGES

axe = Axe()

WCAG_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]


def _format(violations):
    lines = []
    for v in violations:
        targets = ", ".join(str(n["target"]) for n in v["nodes"][:3])
        lines.append(f"[{v['impact']}] {v['id']}: {v['help']} -> {targets}")
    return "\n".join(lines)


@pytest.mark.parametrize("theme", ["light", "dark"])
@pytest.mark.parametrize("path", PAGES)
def test_page_has_no_wcag_violations(page: Page, base_url: str, path: str, theme: str):
    page.emulate_media(reduced_motion="reduce")
    page.add_init_script(f"localStorage.setItem('theme', '{theme}')")
    page.goto(base_url + path)
    # Reveal every section so axe checks what a reader actually sees
    page.evaluate("document.querySelectorAll('.reveal').forEach(el => el.classList.add('visible'))")
    page.wait_for_timeout(700)

    results = axe.run(
        page,
        # The floating code fragments are decorative background art (aria-hidden)
        context={"exclude": [["#codeFragments"]]},
        options={"runOnly": {"type": "tag", "values": WCAG_TAGS}},
    )
    violations = results.response["violations"]
    assert not violations, f"{path} ({theme}) has accessibility violations:\n{_format(violations)}"

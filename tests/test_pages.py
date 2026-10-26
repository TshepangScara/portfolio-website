"""Smoke tests that run against every page of the site."""
import re

import pytest
from playwright.sync_api import Page, expect

from conftest import PAGES


@pytest.mark.parametrize("path", PAGES)
def test_page_loads_with_200(page: Page, base_url: str, path: str):
    response = page.goto(base_url + path)
    assert response is not None and response.status == 200


@pytest.mark.parametrize("path", PAGES)
def test_page_has_no_console_errors(page: Page, base_url: str, console_errors, path: str):
    page.goto(base_url + path)
    page.wait_for_load_state("networkidle")
    assert console_errors == [], f"Console errors on {path}: {console_errors}"


@pytest.mark.parametrize("path", PAGES)
def test_page_has_title_and_meta_description(page: Page, base_url: str, path: str):
    page.goto(base_url + path)
    expect(page).to_have_title(re.compile("Tshepang Molete"))
    description = page.locator("meta[name='description']").get_attribute("content")
    assert description and len(description) > 50


@pytest.mark.parametrize("path", PAGES)
def test_page_has_exactly_one_h1(page: Page, base_url: str, path: str):
    page.goto(base_url + path)
    expect(page.locator("h1")).to_have_count(1)


@pytest.mark.parametrize("path", PAGES)
def test_no_broken_images(page: Page, base_url: str, path: str):
    page.goto(base_url + path)
    images = page.locator("img")
    for i in range(images.count()):
        img = images.nth(i)
        img.scroll_into_view_if_needed()
        img.evaluate("el => el.decode ? el.decode().catch(() => {}) : null")
        natural_width = img.evaluate("el => el.naturalWidth")
        src = img.get_attribute("src")
        assert natural_width > 0, f"Broken image on {path}: {src}"
        assert img.get_attribute("alt"), f"Image without alt text on {path}: {src}"


@pytest.mark.parametrize("path", PAGES)
def test_internal_links_resolve(page: Page, base_url: str, path: str):
    page.goto(base_url + path)
    hrefs = page.eval_on_selector_all(
        "a[href]", "els => els.map(e => e.getAttribute('href'))"
    )
    internal = {
        h.split("#")[0]
        for h in hrefs
        if h and not h.startswith(("http", "mailto:", "tel:", "#"))
    }
    for href in sorted(internal):
        status = page.request.get(base_url + href).status
        assert status == 200, f"{path} links to {href}, which returned {status}"


@pytest.mark.parametrize("path", PAGES)
def test_external_links_open_safely(page: Page, base_url: str, path: str):
    """Links with target=_blank must set rel=noopener to prevent tab-nabbing."""
    page.goto(base_url + path)
    links = page.locator("a[target='_blank']")
    for i in range(links.count()):
        rel = links.nth(i).get_attribute("rel") or ""
        assert "noopener" in rel, f"{links.nth(i).get_attribute('href')} on {path} lacks rel=noopener"

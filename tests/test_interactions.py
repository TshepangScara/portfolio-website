"""Behaviour tests: navigation, dark mode, mobile menu, hero terminal."""
import re

import pytest
from playwright.sync_api import Page, expect

from conftest import PAGES
from pages.base_page import BasePage
from pages.home_page import HomePage


# --- Navigation -------------------------------------------------------------

def test_nav_links_navigate_to_each_page(page: Page, base_url: str):
    site = BasePage(page, base_url).open()
    expect(site.nav_links).to_have_count(len(PAGES))
    for path in PAGES:
        site.open()
        page.locator(f".nav-links a[href='{path}']").click()
        expect(page).to_have_url(re.compile(re.escape(path) + "$"))


@pytest.mark.parametrize("path", PAGES)
def test_current_page_is_marked_active(page: Page, base_url: str, path: str):
    BasePage(page, base_url).open(path)
    expect(page.locator(f".nav-links a[href='{path}']")).to_have_class(re.compile(r"\bactive\b"))


# --- Dark mode ----------------------------------------------------------------

def test_theme_toggle_switches_to_dark(page: Page, base_url: str):
    site = BasePage(page, base_url).open()
    assert not site.is_dark()
    site.toggle_theme()
    assert site.is_dark()
    expect(site.theme_toggle).to_have_attribute("aria-pressed", "true")


def test_theme_choice_persists_across_pages(page: Page, base_url: str):
    site = BasePage(page, base_url).open()
    site.toggle_theme()
    site.open("projects.html")
    assert site.is_dark(), "Dark mode should persist when navigating"
    page.reload()
    assert site.is_dark(), "Dark mode should persist after reload"


# --- Mobile ---------------------------------------------------------------------

@pytest.fixture
def mobile_page(page: Page):
    page.set_viewport_size({"width": 390, "height": 844})
    return page


def test_hamburger_opens_and_closes_menu(mobile_page: Page, base_url: str):
    site = BasePage(mobile_page, base_url).open()
    expect(site.hamburger).to_be_visible()
    expect(site.hamburger).to_have_attribute("aria-expanded", "false")

    site.hamburger.click()
    expect(site.hamburger).to_have_attribute("aria-expanded", "true")
    expect(site.nav_links.first).to_be_visible()

    site.hamburger.click()
    expect(site.hamburger).to_have_attribute("aria-expanded", "false")


@pytest.mark.parametrize("path", PAGES)
def test_no_horizontal_scroll_on_mobile(mobile_page: Page, base_url: str, path: str):
    BasePage(mobile_page, base_url).open(path)
    overflow = mobile_page.evaluate(
        "document.documentElement.scrollWidth - document.documentElement.clientWidth"
    )
    assert overflow <= 0, f"{path} scrolls sideways by {overflow}px on a 390px screen"


# --- Hero terminal --------------------------------------------------------------

def test_terminal_runs_and_reports_all_passed(page: Page, base_url: str):
    home = HomePage(page, base_url).open()
    home.wait_for_run_to_finish()
    expect(home.passed_lines).to_have_count(5)
    expect(home.terminal_body).to_contain_text("5 passed")
    expect(home.terminal_body).not_to_contain_text("FAILED")


def test_terminal_rerun_restarts_the_suite(page: Page, base_url: str):
    home = HomePage(page, base_url).open()
    home.wait_for_run_to_finish()
    expect(home.rerun_button).to_be_enabled()

    home.rerun_button.click()
    expect(home.terminal).to_have_attribute("data-state", "running")
    expect(home.rerun_button).to_be_disabled()

    home.wait_for_run_to_finish()
    expect(home.passed_lines).to_have_count(5)


def test_terminal_respects_reduced_motion(browser, base_url: str):
    context = browser.new_context(reduced_motion="reduce")
    page = context.new_page()
    try:
        home = HomePage(page, base_url).open()
        # With reduced motion the whole run renders at once, no typing animation
        home.wait_for_run_to_finish(timeout=1_500)
        expect(home.passed_lines).to_have_count(5)
    finally:
        context.close()

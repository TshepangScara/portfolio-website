"""Page object for the elements every page shares: header nav, theme toggle, footer."""
from playwright.sync_api import Page, Locator


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    # --- navigation -------------------------------------------------------
    def open(self, path: str = "index.html") -> "BasePage":
        self.page.goto(self.base_url + path)
        return self

    @property
    def nav_links(self) -> Locator:
        return self.page.locator(".nav-links a")

    @property
    def hamburger(self) -> Locator:
        return self.page.locator("#navHamburger")

    # --- theme --------------------------------------------------------------
    @property
    def theme_toggle(self) -> Locator:
        return self.page.locator("#themeToggle")

    def is_dark(self) -> bool:
        return self.page.evaluate("document.body.classList.contains('dark-mode')")

    def toggle_theme(self) -> None:
        self.theme_toggle.click()

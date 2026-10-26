"""Page object for the home page and its hero terminal."""
from playwright.sync_api import Locator

from .base_page import BasePage


class HomePage(BasePage):
    def open(self, path: str = "index.html") -> "HomePage":
        super().open(path)
        return self

    @property
    def terminal(self) -> Locator:
        return self.page.get_by_test_id("hero-terminal")

    @property
    def terminal_body(self) -> Locator:
        return self.page.locator("#terminalBody")

    @property
    def rerun_button(self) -> Locator:
        return self.page.locator("#terminalRerun")

    @property
    def passed_lines(self) -> Locator:
        return self.terminal_body.locator(".t-pass")

    def wait_for_run_to_finish(self, timeout: int = 15_000) -> None:
        self.page.locator("#heroTerminal[data-state='done']").wait_for(timeout=timeout)

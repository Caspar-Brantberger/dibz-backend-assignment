from __future__ import annotations

from dataclasses import dataclass

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@dataclass
class PlatformSession:
    base_url: str

    def login(self, username: str, password: str) -> None:
        """Login to the platform using the given credentials."""
        raise NotImplementedError

    def fetch_account_html(self) -> str:
        """Return the account HTML after login.

        TODO:
        - Use the authenticated requests session to GET /account.
        - Return the response text.
        """
        raise NotImplementedError

    def open_account_in_browser(self) -> None:
        """Optional helper to inspect the page manually with Selenium.

        This is not required to solve the assignment, but it reflects the kind of
        tooling the team uses in production.
        """
        options = Options()
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(f"{self.base_url}/account")
            print(driver.title)
        finally:
            driver.quit()


def build_session(base_url: str) -> PlatformSession:
    return PlatformSession(base_url=base_url.rstrip("/"))

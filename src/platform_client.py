from __future__ import annotations

from dataclasses import dataclass

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@dataclass
class PlatformSession:
    session: requests.Session
    base_url: str

    def login(self, username: str, password: str) -> None:
        """Login to the platform using the given credentials."""
        login_url = f"{self.base_url}/login"

        response =self.session.post(login_url, data={"username": username, "password": password})

        if response.status_code != 200:
            raise RuntimeError(f"Login failed with status code {response.status_code}")

    def fetch_account_html(self) -> str:
        """Return the account HTML after login.

        TODO:
        - Use the authenticated requests session to GET /account.
        - Return the response text.
        """
        account_url = f"{self.base_url}/account"
        response = self.session.get(account_url)

        if response.status_code != 200:
            raise RuntimeError(f"Failed to fetch account page with status code {response.status_code}")

        return response.text

    def open_account_in_browser(self) -> None:
        """Optional helper to inspect the page manually with Selenium.

        This is not required to solve the assignment, but it reflects the kind of
        tooling the team uses in production.
        """
        options = Options()
        options.add_argument("-no-sandbox")
        driver = webdriver.Chrome(options=options)
        try:
            driver.get(f"{self.base_url}/account")
            print(driver.title)
        finally:
            driver.quit()


def build_session(base_url: str) -> PlatformSession:
    return PlatformSession(session=requests.Session(), base_url=base_url.rstrip("/"))

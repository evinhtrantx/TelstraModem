"""Selenium-based login helper for the gateway web UI."""

from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.chrome import ChromeDriverManager


def create_chrome_driver(headless: bool = True, timeout: int = 30) -> WebDriver:
    """Return a Chrome WebDriver configured for automation."""

    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    driver.set_page_load_timeout(timeout)
    return driver


class LoginPage:
    """Page object for the gateway login page.

    Example usage:

        driver = create_chrome_driver()
        page = LoginPage(driver)
        success = page.login("http://mygateway.gateway/login.lp", "admin", "password")
    """

    def __init__(self, driver: WebDriver, timeout: float = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def login(self, url: str, username: str, password: str, *, wait_for_redirect: bool = True) -> bool:
        """Navigate to the login URL and authenticate.

        Returns True if the page navigated away from the login page (likely success),
        or False if it stayed on the login page (likely failure or timeout).
        """

        self.driver.get(url)

        user_field = self.wait.until(EC.presence_of_element_located((By.ID, "srp_username")))
        pass_field = self.wait.until(EC.presence_of_element_located((By.ID, "srp_password")))

        user_field.clear()
        user_field.send_keys(username)
        pass_field.clear()
        pass_field.send_keys(password)

        submit = self.wait.until(EC.element_to_be_clickable((By.ID, "sign-me-in")))
        submit.click()

        if not wait_for_redirect:
            return True

        try:
            # Wait for a strong indicator that the login succeeded.
            # The post-login page includes a logout link with id "signout".
            self.wait.until(EC.presence_of_element_located((By.ID, "signout")))
            return True
        except Exception:
            return False

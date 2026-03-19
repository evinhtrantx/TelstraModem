"""CLI script to login and control guest WiFi."""

import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from wifi.ctl import HostInfo, LoginPage, create_chrome_driver


def main():
    if len(sys.argv) != 2:
        print("Usage: python -m myapp <on|off|toggle>")
        sys.exit(1)

    action = sys.argv[1].lower()
    if action not in ('on', 'off', 'toggle'):
        print("First argument must be 'on', 'off', or 'toggle'")
        sys.exit(1)

    username = HostInfo.USERNAME
    password = os.environ['GATEWAY_PASSWORD']

    driver = create_chrome_driver(headless=True)
    try:
        # Login
        login_url = HostInfo.BASE + HostInfo.LOGIN_PATH
        page = LoginPage(driver)
        success = page.login(login_url, username, password)
        if not success:
            print("Login failed. Check credentials and try again.")
            return

        # Navigate to WiFi control page
        wifi_url = HostInfo.BASE + HostInfo.WIFI_CONTROL_PATH
        driver.get(wifi_url)

        # Get the checkbox
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_enabled"))
        )

        # Toggle based on action
        if action == 'on' and not checkbox.is_selected():
            checkbox.click()
        elif action == 'off' and checkbox.is_selected():
            checkbox.click()
        elif action == 'toggle':
            checkbox.click()
        
        # Click Save
        save_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "save-config"))
        )
        save_button.click()

        # Wait for settings to apply
        if action == 'on':
            WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.ID, "ap_enabled").is_selected()
            )
            print("successfully enable wifi")
        else:
            WebDriverWait(driver, 10).until(
                lambda d: not d.find_element(By.ID, "ap_enabled").is_selected()
            )
            print("successfully disable wifi")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()

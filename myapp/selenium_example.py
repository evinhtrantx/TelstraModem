from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_chrome_driver(headless=True):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=opts)


def fetch_title(url, headless=True):
    driver = get_chrome_driver(headless=headless)
    try:
        driver.get(url)
        return driver.title
    finally:
        driver.quit()


if __name__ == "__main__":
    # Simple CLI for manual testing
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://example.com"
    print(fetch_title(url))

import shutil
import pytest

from myapp.selenium_example import fetch_title


chrome_bins = ["chrome", "google-chrome", "chromium", "chrome.exe", "msedge.exe"]
HAS_BROWSER = any(shutil.which(b) for b in chrome_bins)


@pytest.mark.skipif(not HAS_BROWSER, reason="No Chrome/Chromium/MS Edge binary found in PATH")
def test_fetch_title_headless():
    title = fetch_title("https://example.com")
    assert "Example Domain" in title

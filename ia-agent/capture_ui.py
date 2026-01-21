import subprocess
import time
from playwright.sync_api import sync_playwright

def capture():
    subprocess.Popen(
        ["uvicorn", "app.main:app", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(3)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8000")
        page.screenshot(path="ia-artifacts/screenshot.png")
        browser.close()

if __name__ == "__main__":
    capture()

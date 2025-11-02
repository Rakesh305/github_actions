# tests/helium_test.py
from helium import *
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import os

def validate_chromedriver():
    try:
        print("Starting Chrome via Helium...")

        # Configure Chrome options for CI
        options = Options()
        options.add_argument("--headless=new")  # new headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = start_chrome(options=options)
        print("Chrome started successfully!")

        # go_to("https://example.com")
        # print("Navigation successful. Page title:", driver.title)
        
        #-----------------------------------
        go_to("https://analyticsstudio.visualdesigner.dnb.com/#/webapps")
        click("login with SSO")

        write("bannaravurir@dnb.com", into="Username")
        click("Remember my username")
        click("Continue")
        time.sleep(5)

        write("bannaravurir@dnb.com", into="Sign in")
        click("next")
        time.sleep(3)

        write("", into="Enter password")
        click("Sign in")
        time.sleep(17)
        #---------------------------------

        os.makedirs("artifacts/screenshots", exist_ok=True)
        screenshot_path = os.path.join("artifacts/screenshots", "example.png")
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

        kill_browser()
        print("Browser closed successfully.")
        return True

    except WebDriverException as e:
        print("Chromedriver validation failed:", e)
        return False


if __name__ == "__main__":
    success = validate_chromedriver()
    if not success:
        raise SystemExit("Chromedriver validation failed.")

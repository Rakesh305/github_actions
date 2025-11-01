# helium_test.py
from helium import start_chrome, go_to, kill_browser
from selenium.common.exceptions import WebDriverException
import os

def validate_chromedriver():
    try:
        print("Starting Chrome via Helium...")
        driver = start_chrome(headless=True)  # Headless for CI
        print("Chrome started successfully!")

        go_to("https://example.com")
        print("Navigation successful. Page title:", driver.title)

        # Save screenshot
        screenshot_path = os.path.join(os.getcwd(), "screenshot.png")
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

import unittest
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class TestMuambatorApp(unittest.TestCase):
    # Wait times
    DEFAULT_WAIT = 10
    SHORT_WAIT = 5

    # Element IDs
    PACKAGE_CODE_FIELD = "br.com.muambator.android:id/package_form_text_code"
    PACKAGE_NAME_FIELD = "br.com.muambator.android:id/package_form_text_name"
    LOGIN_USERNAME_FIELD = "br.com.muambator.android:id/login_username"
    LOGIN_PASSWORD_FIELD = "br.com.muambator.android:id/login_password"
    LOGIN_CONFIRM_BUTTON = "br.com.muambator.android:id/login_confirm"
    ERROR_MESSAGE = "android:id/message"
    ERROR_CLOSE_BUTTON = "android:id/button1"
    ALERT_TITLE = "br.com.muambator.android:id/alertTitle"

    def setUp(self):
        options = AppiumOptions()
        options.load_capabilities({
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:appPackage": "br.com.muambator.android",
            "appium:appActivity": ".ui.activity.ListPackageActivity",
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:connectHardwareKeyboard": True
        })

        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        self.driver.implicitly_wait(self.DEFAULT_WAIT)

    def tearDown(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def debug_print(self, message):
        if hasattr(self, 'debug') and self.debug:
            print(f"DEBUG: {message}")

    def test_add_and_delete_package(self):
        """Test adding a new package and then deleting it."""
        self.debug = True
        package_code = "BR1234567890BR"
        package_name = "Test Package"

        self.debug_print("Cenário 1: Login")
        self.login("lfsdias", "teste123")

        self.debug_print("Adding new package")
        try:
            # Add package
            add_button = WebDriverWait(self.driver, self.DEFAULT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Add package"))
            )
            add_button.click()

            code_field = self.driver.find_element(by=AppiumBy.ID, value=self.PACKAGE_CODE_FIELD)
            code_field.click()
            code_field.send_keys(package_code)

            name_field = self.driver.find_element(by=AppiumBy.ID, value=self.PACKAGE_NAME_FIELD)
            name_field.click()
            name_field.send_keys(package_name)

            confirm_button = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Confirm")
            confirm_button.click()

            # Handle advertisement if present
            self.handle_advertisement()

            # Verify package was added
            self.verify_package_in_pending_list(package_name)

            # Delete package
            self.delete_package(package_name)

        except (TimeoutException, NoSuchElementException) as e:
            self.fail(f"Test failed: {str(e)}")

    def handle_advertisement(self):
        """Handles any advertisements that appear."""
        self.debug_print("Handling advertisement")
        try:
            # Try to skip video first
            try:
                skip_video = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.TextView[@text='Skip video']"))
                )
                skip_video.click()
                time.sleep(self.SHORT_WAIT)
            except TimeoutException:
                self.debug_print("No skip video button found")

            # Try to close advertisement
            try:
                close_button = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                    EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.Button"))
                )
                close_button.click()
            except TimeoutException:
                self.debug_print("No close button found")

        except Exception as e:
            self.debug_print(f"Error handling advertisement: {str(e)}")

    def verify_package_in_pending_list(self, package_name):
        """Verifies if a package appears in the pending list."""
        self.debug_print(f"Verifying package in pending list: {package_name}")
        try:
            pending_button = WebDriverWait(self.driver, self.DEFAULT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.Button"))
            )
            pending_button.click()

            package_element = WebDriverWait(self.driver, self.DEFAULT_WAIT).until(
                EC.presence_of_element_located(
                    (AppiumBy.XPATH, f"//android.widget.TextView[@text='{package_name}']")
                )
            )
            self.assertTrue(package_element.is_displayed(), f"Package {package_name} not found in pending list")

        except TimeoutException:
            self.fail(f"Package {package_name} not found in pending list")

    def delete_package(self, package_name):
        """Deletes a package from the list."""
        self.debug_print(f"Deleting package: {package_name}")
        try:
            package_element = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, f"//android.widget.TextView[@text='{package_name}']"))
            )
            package_element.click()

            more_options = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "More options"))
            )
            more_options.click()

            delete_option = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, 
                    "//android.widget.TextView[@resource-id='br.com.muambator.android:id/title' and @text='Delete']"))
            )
            delete_option.click()

            confirm_button = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.ID, self.ERROR_CLOSE_BUTTON))
            )
            confirm_button.click()

        except TimeoutException as e:
            self.fail(f"Failed to delete package {package_name}: {str(e)}")

if __name__ == '__main__':
    unittest.main()

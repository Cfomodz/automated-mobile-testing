from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import pytest

class TestMuambator:
    # Wait times
    DEFAULT_WAIT = 10
    SHORT_WAIT = 2

    # Test Data
    USERNAME = "lfdias"
    PASSWORD = "teste123"

    # Element IDs
    LOGIN_BUTTON = "//android.widget.Button[@text=\"Faça login!\"]"
    LOGIN_USERNAME = "br.com.muambator.android:id/login_username"
    LOGIN_PASSWORD = "br.com.muambator.android:id/login_password"
    LOGIN_FORM = "br.com.muambator.android:id/form"
    LOGIN_CONFIRM = "br.com.muambator.android:id/login_confirm"
    PREFERENCES_BUTTON = "Preferências"

    @pytest.fixture(scope="function")
    def setup(self):
        """Setup for each test case."""
        self.options = AppiumOptions()
        self.options.load_capabilities({
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:appPackage": "br.com.muambator.android",
            "appium:appActivity": ".ui.activity.ListPackageActivity",
            "appium:ensureWebviewsHavePages": True,
            "appium:nativeWebScreenshot": True,
            "appium:newCommandTimeout": 3600,
            "appium:connectHardwareKeyboard": True
        })

        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=self.options)
        self.logger = logging.getLogger(__name__)
        yield
        self.driver.quit()

    def test_login_and_navigate(self, setup):
        """Test login flow and navigation to preferences."""
        try:
            # Login
            self.logger.info("Starting login process")
            login_button = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, self.LOGIN_BUTTON))
            )
            login_button.click()

            # Enter username
            username_field = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.presence_of_element_located((AppiumBy.ID, self.LOGIN_USERNAME))
            )
            username_field.click()
            username_field.send_keys(self.USERNAME)

            # Enter password
            password_field = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.presence_of_element_located((AppiumBy.ID, self.LOGIN_PASSWORD))
            )
            password_field.click()
            password_field.send_keys(self.PASSWORD)

            # Click form and confirm
            form = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.presence_of_element_located((AppiumBy.ID, self.LOGIN_FORM))
            )
            form.click()

            confirm_button = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.ID, self.LOGIN_CONFIRM))
            )
            confirm_button.click()
            self.logger.info("Login completed successfully")

            # Navigate to preferences
            preferences = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, self.PREFERENCES_BUTTON))
            )
            preferences.click()
            self.logger.info("Successfully navigated to preferences")

        except TimeoutException as e:
            self.logger.error(f"Timeout waiting for element: {str(e)}")
            raise
        except NoSuchElementException as e:
            self.logger.error(f"Element not found: {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error occurred: {str(e)}")
            raise

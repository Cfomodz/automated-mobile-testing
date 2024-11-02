import unittest
import logging
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TesteMuambatorApp(unittest.TestCase):
    # Wait times
    DEFAULT_WAIT = 10
    SHORT_WAIT = 5

    # Element IDs
    LOGIN_USERNAME_FIELD = "br.com.muambator.android:id/login_username"
    LOGIN_PASSWORD_FIELD = "br.com.muambator.android:id/login_password"
    LOGIN_CONFIRM_BUTTON = "br.com.muambator.android:id/login_confirm"
    MESSAGE_FIELD = "android:id/message"
    CONFIRM_BUTTON = "android:id/button1"

    def setUp(self):
        """Configure and initialize the Appium driver."""
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
        self.logger = logging.getLogger(__name__)

    def tearDown(self):
        """Clean up after each test."""
        if self.driver:
            self.driver.quit()

    def test_login_and_navigate_to_preferences(self):
        """Test successful login and navigation to preferences screen."""
        try:
            # Login steps
            self.logger.info("Starting login process")
            login_button = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.Button[@text=\"Faça login!\"]"))
            )
            login_button.click()

            # Enter credentials
            username_field = self.driver.find_element(by=AppiumBy.ID, value=self.LOGIN_USERNAME_FIELD)
            username_field.click()
            username_field.send_keys("lfsdias")

            password_field = self.driver.find_element(by=AppiumBy.ID, value=self.LOGIN_PASSWORD_FIELD)
            password_field.click()
            password_field.send_keys("teste123")

            # Confirm login
            confirm_button = self.driver.find_element(by=AppiumBy.ID, value=self.LOGIN_CONFIRM_BUTTON)
            confirm_button.click()

            # Navigate to Preferences
            self.logger.info("Navigating to Preferences")
            preferences_button = WebDriverWait(self.driver, self.DEFAULT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Preferências"))
            )
            preferences_button.click()

            # Verify username
            self.logger.info("Verifying username display")
            username_text = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.presence_of_element_located((AppiumBy.XPATH, "//android.widget.TextView[@text=\"Olá, lfsdias\"]"))
            )
            self.assertTrue(username_text.is_displayed(), "Username not displayed in Preferences screen")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise

    def test_logout_and_return_to_home(self):
        """Test logout functionality and return to home screen."""
        try:
            # Perform login first
            self.test_login_and_navigate_to_preferences()

            # Initiate logout
            self.logger.info("Starting logout process")
            username_element = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.TextView[@text=\"Olá, leonardoodias\"]"))
            )
            username_element.click()

            # Verify logout message
            message_element = self.driver.find_element(by=AppiumBy.ID, value=self.MESSAGE_FIELD)
            self.assertTrue(message_element.is_displayed(), "Logout confirmation message not found")
            self.assertEqual(message_element.text, "Deseja realmente sair da sua conta?")

            # Confirm logout
            self.logger.info("Confirming logout")
            logout_button = WebDriverWait(self.driver, self.SHORT_WAIT).until(
                EC.element_to_be_clickable((By.ID, self.CONFIRM_BUTTON))
            )
            logout_button.click()

            # Verify return to home screen
            self.logger.info("Verifying return to home screen")
            new_account_text = WebDriverWait(self.driver, self.DEFAULT_WAIT).until(
                EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text=\"Nova conta\"]"))
            )
            self.assertTrue(new_account_text.is_displayed(), "Failed to return to home screen after logout")

        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Test failed: {str(e)}")
            raise

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main()

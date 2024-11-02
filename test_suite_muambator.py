import logging
import unittest
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from app_utils import AppUtils
from config import (
    TEST_USERNAME, 
    TEST_PASSWORD, 
    TEST_PACKAGE_CODE, 
    TEST_PACKAGE_NAME,
    CAPABILITIES,
    APPIUM_URL,
    DEFAULT_WAIT,
    SHORT_WAIT
)
from locators import (
    HELLO_USER_PT,
    LOGIN_PAGE,
    NEW_ACCOUNT_BUTTON,
    SNACKBAR_TEXT
)

class TestMuambatorApp(unittest.TestCase):
    def setUp(self):
        """Initialize test environment and Appium driver."""
        options = AppiumOptions()
        options.load_capabilities(CAPABILITIES)
        self.driver = webdriver.Remote(APPIUM_URL, options=options)
        self.driver.implicitly_wait(DEFAULT_WAIT)
        self.app_utils = AppUtils(self.driver)
        self.logger = logging.getLogger(__name__)

    def tearDown(self):
        """Clean up after each test."""
        if hasattr(self, 'driver'):
            self.driver.quit()

    def test_login_success(self):
        """Test successful login and navigation to Preferences screen."""
        self.logger.info("Starting login success test")
        
        # Perform login
        self.app_utils.login(TEST_USERNAME, TEST_PASSWORD)
        self.app_utils.navigate_to_preferences()

        # Verify username on Preferences screen
        self.logger.info("Verifying username on Preferences screen")
        el_hello_user = WebDriverWait(self.driver, DEFAULT_WAIT).until(
            EC.visibility_of_element_located(HELLO_USER_PT(TEST_USERNAME))
        )
        self.assertTrue(
            el_hello_user.is_displayed(), 
            "Username not found on Preferences screen"
        )

    def test_login_invalid_password(self):
        """Test login failure with invalid password."""
        self.logger.info("Starting invalid password test")
        invalid_password = "senha incorreta"

        # Attempt login with invalid password
        self.app_utils.login(TEST_USERNAME, invalid_password)
        self.app_utils.close_error_message()

        # Verify return to login screen
        self.logger.info("Verifying return to login screen")
        el_login_page = WebDriverWait(self.driver, DEFAULT_WAIT).until(
            EC.visibility_of_element_located(LOGIN_PAGE)
        )
        self.assertTrue(
            el_login_page.is_displayed(), 
            "Failed to return to login screen after error"
        )

    def test_login_invalid_username(self):
        """Test login failure with invalid username."""
        self.logger.info("Starting invalid username test")
        invalid_username = "Kx9"

        # Attempt login with invalid username
        self.app_utils.login(invalid_username, TEST_PASSWORD)
        self.app_utils.close_error_message()

        # Verify return to login screen
        self.logger.info("Verifying return to login screen")
        el_login_page = WebDriverWait(self.driver, DEFAULT_WAIT).until(
            EC.visibility_of_element_located(LOGIN_PAGE)
        )
        self.assertTrue(
            el_login_page.is_displayed(), 
            "Failed to return to login screen after error"
        )

    def test_logout_success(self):
        """Test successful logout and return to initial screen."""
        self.logger.info("Starting logout test")

        # Login and navigate to preferences
        self.app_utils.login(TEST_USERNAME, TEST_PASSWORD)
        self.app_utils.navigate_to_preferences()
        
        # Perform logout
        self.app_utils.logout(TEST_USERNAME)

        # Verify return to initial screen
        self.logger.info("Verifying return to initial screen")
        el_new_account_button = WebDriverWait(self.driver, DEFAULT_WAIT).until(
            EC.visibility_of_element_located(NEW_ACCOUNT_BUTTON)
        )
        self.assertTrue(
            el_new_account_button.is_displayed(), 
            "Failed to return to initial screen after logout"
        )

    def test_add_new_package_success(self):
        """Test successful package addition."""
        self.logger.info("Starting add package test")

        # Login and add package
        self.app_utils.login(TEST_USERNAME, TEST_PASSWORD)
        self.app_utils.add_new_package(TEST_PACKAGE_CODE, TEST_PACKAGE_NAME)

        # Verify package was added successfully
        self.logger.info("Verifying package addition")
        self.app_utils.verify_added_package_pending(TEST_PACKAGE_NAME)

    def test_delete_package_pending_success(self):
        """Test successful package deletion."""
        self.logger.info("Starting delete package test")
        package_to_delete = "Pacote Automatizad1"

        # Login and delete package
        self.app_utils.login(TEST_USERNAME, TEST_PASSWORD)
        self.app_utils.delete_package_pending(package_to_delete)

        # Verify successful deletion
        self.logger.info("Verifying successful deletion")
        success_message = WebDriverWait(self.driver, SHORT_WAIT).until(
            EC.presence_of_element_located(SNACKBAR_TEXT)
        )
        expected_message = f"Pacote '{package_to_delete}' excluído com sucesso."
        self.assertEqual(
            success_message.text,
            expected_message,
            "Incorrect deletion success message"
        )

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    unittest.main()

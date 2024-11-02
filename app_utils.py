import logging
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import DEFAULT_WAIT, SHORT_WAIT
from locators import *  # Import all locators

class AppUtils:
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)

    def login(self, username, password):
        """Performs login to the application."""
        try:
            self.logger.info("Attempting login")
            login_button = WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.element_to_be_clickable(LOGIN_BUTTON)
            )
            login_button.click()

            username_field = self.driver.find_element(*LOGIN_USERNAME_FIELD)
            username_field.click()
            username_field.send_keys(username)

            password_field = self.driver.find_element(*LOGIN_PASSWORD_FIELD)
            password_field.click()
            password_field.send_keys(password)

            login_confirm = self.driver.find_element(*LOGIN_CONFIRM_BUTTON)
            login_confirm.click()
            
            self.logger.info("Login successful")
            
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Failed to login: {str(e)}")
            raise

    def navigate_to_preferences(self):
        """Navigates to the Preferences screen."""
        try:
            self.logger.info("Navigating to Preferences")
            preferences_button = WebDriverWait(self.driver, DEFAULT_WAIT).until(
                EC.element_to_be_clickable(PREFERENCES_BUTTON)
            )
            preferences_button.click()
            self.logger.info("Successfully navigated to Preferences")
            
        except TimeoutException as e:
            self.logger.error("Failed to navigate to preferences: Timeout waiting for button")
            raise
    def logout(self, username):
        """Performs logout from the application."""
        try:
            self.logger.info("Initiating logout process")
            hello_user = WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.element_to_be_clickable(HELLO_USER(username))
            )
            hello_user.click()
            
            message_element = WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.visibility_of_element_located(ERROR_MESSAGE)
            )
            message = message_element.text
            assert message == "Do you really want to sign out?", "Unexpected logout confirmation message"

            self.logger.info("Confirming logout")
            logout_button = WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.element_to_be_clickable(ERROR_CLOSE_BUTTON)
            )
            logout_button.click()
            self.logger.info("Logout successful")
            
        except (TimeoutException, AssertionError) as e:
            self.logger.error(f"Logout failed: {str(e)}")
            raise

    def close_error_message(self):
        """Closes the error message window."""
        try:
            self.logger.info("Waiting for the error message to appear")
            error_message = WebDriverWait(self.driver, DEFAULT_WAIT).until(
                EC.presence_of_element_located(ERROR_MESSAGE)
            )

            message = error_message.text
            self.logger.info(f"Error message found: {message}")

            self.logger.info("Clicking the error message to close")
            error_message.click()

            self.logger.info("Waiting for the close button to appear")
            close_button = WebDriverWait(self.driver, DEFAULT_WAIT).until(
                EC.element_to_be_clickable(ERROR_CLOSE_BUTTON)
            )
            self.logger.info("Clicking the close button")
            close_button.click()

        except TimeoutException:
            self.logger.error("Timeout while trying to close the error message")
            raise
        except StaleElementReferenceException:
            self.logger.error("Element became stale while trying to close the error message")
            raise

    def add_new_package(self, package_code, package_name):
        """Adds a new package to the tracking system."""
        try:
            self.logger.info(f"Adding new package: {package_name}")
            add_button = WebDriverWait(self.driver, DEFAULT_WAIT).until(
                EC.element_to_be_clickable(ADD_PACKAGE_BUTTON)
            )
            add_button.click()

            code_field = self.driver.find_element(*PACKAGE_CODE_FIELD)
            code_field.click()
            code_field.send_keys(package_code)

            name_field = self.driver.find_element(*PACKAGE_NAME_FIELD)
            name_field.click()
            name_field.send_keys(package_name)

            confirm_button = self.driver.find_element(*CONFIRM_BUTTON)
            confirm_button.click()

            self.logger.debug("Waiting for advertisement page")
            self.interact_with_advertisement()

            self.logger.debug("Verifying package addition")
            self.verify_advertisement_screen_closed()
            self.verify_added_package_pending(package_name)
            
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Failed to add package: {str(e)}")
            raise

    def interact_with_advertisement(self):
        """Interacts with advertisement if present."""
        try:
            try:
                self.logger.debug("Attempting to find Skip Video button")
                skip_video_button = WebDriverWait(self.driver, SHORT_WAIT).until(
                    EC.element_to_be_clickable(SKIP_VIDEO_BUTTON)
                )
                skip_video_button.click()
                self.logger.debug("Skip Video clicked, waiting for close button")
                
                time.sleep(SHORT_WAIT)

                try:
                    close_button = WebDriverWait(self.driver, SHORT_WAIT).until(
                        EC.element_to_be_clickable(CLOSE_BUTTON)
                    )
                    close_button.click()
                    self.logger.debug("Close button clicked after video skip")

                except TimeoutException:
                    self.logger.warning("Close button not found after skipping video")

            except TimeoutException:
                self.logger.debug("Skip Video not found, trying direct close")
                try:
                    close_button = WebDriverWait(self.driver, SHORT_WAIT).until(
                        EC.element_to_be_clickable(CLOSE_BUTTON)
                    )
                    close_button.click()
                    self.logger.debug("Direct close button clicked")

                except TimeoutException:
                    self.logger.warning("Direct close button not found")

        except NoSuchElementException:
            self.logger.info("No advertisement elements found or actions necessary")

    def verify_advertisement_screen_closed(self):
        """Verifies if the advertisement screen was closed correctly."""
        try:
            close_button = WebDriverWait(self.driver, DEFAULT_WAIT).until(
                EC.presence_of_element_located(CLOSE_BUTTON)
            )

            if close_button.is_displayed():
                self.logger.debug("Advertisement screen closed correctly")
                close_button.click()
            else:
                self.logger.warning("Advertisement screen not closed correctly")
                
        except TimeoutException:
            self.logger.error("Timeout while verifying advertisement screen closure")
            raise

    def verify_added_package_pending(self, package_name):
        """Verifies if the package was correctly added to the pending list."""
        try:
            pending_button = WebDriverWait(self.driver, DEFAULT_WAIT).until(
                EC.element_to_be_clickable(PENDING_BUTTON)
            )
            pending_button.click()

            WebDriverWait(self.driver, DEFAULT_WAIT).until(
                EC.presence_of_element_located(PENDING_LAYOUT)
            )

            self.logger.debug(f"Verifying package: {package_name}")
            package_element = self.driver.find_element(*PACKAGE_ITEM(package_name))

            if package_element.is_displayed():
                self.logger.info(f"Package {package_name} found in pending list")
            else:
                self.logger.warning(f"Package {package_name} in DOM but not visible")
                
        except TimeoutException:
            self.logger.error("Timeout while verifying package in pending list")
            raise
        except NoSuchElementException:
            self.logger.error(f"Package {package_name} not found in pending list")
            raise

    def delete_package_pending(self, package_name_to_delete):
        """Deletes a package from the pending list."""
        try:
            self.logger.info(f"Attempting to delete package: {package_name_to_delete}")
            package_element = WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.element_to_be_clickable(PACKAGE_ITEM(package_name_to_delete))
            )
            package_element.click()

            more_options_button = WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.element_to_be_clickable(MORE_OPTIONS_BUTTON)
            )
            more_options_button.click()

            delete_option = WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.element_to_be_clickable(DELETE_OPTION)
            )
            delete_option.click()

            WebDriverWait(self.driver, SHORT_WAIT).until(
                EC.visibility_of_element_located(ALERT_TITLE)
            )

            confirm_button = self.driver.find_element(*ERROR_CLOSE_BUTTON)
            confirm_button.click()
            
            time.sleep(SHORT_WAIT)
            self.logger.info(f"Successfully deleted package: {package_name_to_delete}")

        except TimeoutException:
            self.logger.error(f"Package '{package_name_to_delete}' not found for deletion")
            raise
        except NoSuchElementException:
            self.logger.error(f"UI element not found while deleting '{package_name_to_delete}'")
            raise


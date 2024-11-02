import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test Configuration
TEST_USERNAME = os.getenv('TEST_USERNAME')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')
TEST_PACKAGE_CODE = os.getenv('TEST_PACKAGE_CODE')
TEST_PACKAGE_NAME = os.getenv('TEST_PACKAGE_NAME')

# Appium Configuration
APPIUM_HOST = os.getenv('APPIUM_HOST', 'http://127.0.0.1')
APPIUM_PORT = os.getenv('APPIUM_PORT', '4723')
APPIUM_URL = f"{APPIUM_HOST}:{APPIUM_PORT}"

# App Configuration
APP_PACKAGE = os.getenv('APP_PACKAGE')
APP_ACTIVITY = os.getenv('APP_ACTIVITY')

# Default Wait Times
DEFAULT_WAIT = 10
SHORT_WAIT = 5

# Appium Capabilities
CAPABILITIES = {
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": APP_PACKAGE,
    "appium:appActivity": APP_ACTIVITY,
    "appium:ensureWebviewsHavePages": True,
    "appium:nativeWebScreenshot": True,
    "appium:newCommandTimeout": 3600,
    "appium:connectHardwareKeyboard": True
} 
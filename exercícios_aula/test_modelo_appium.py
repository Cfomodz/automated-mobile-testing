# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
import time


# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

options = AppiumOptions()
# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

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

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

time.sleep(2)

el7 = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Button[@text=\"Faça login!\"]")
el7.click()
time.sleep(2)

el8 = driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_username")
el8.click()
el8.send_keys("leonardoodias")
time.sleep(2)

el9 = driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_password")
el9.click()
el9.send_keys("Ldias@2024")
time.sleep(2)

el10 = driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/form")
el10.click()
time.sleep(3)

el11 = driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_confirm")
el11.click()

time.sleep(5)

el12 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Preferências")
el12.click()

time.sleep(5)

driver.quit()
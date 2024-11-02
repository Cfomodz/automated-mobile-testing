from appium.webdriver.common.by import By as AppiumBy

# Login related elements
LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text=\"Login!\"]")
LOGIN_USERNAME_FIELD = (AppiumBy.ID, "br.com.muambator.android:id/login_username")
LOGIN_PASSWORD_FIELD = (AppiumBy.ID, "br.com.muambator.android:id/login_password")
LOGIN_CONFIRM_BUTTON = (AppiumBy.ID, "br.com.muambator.android:id/login_confirm")
HELLO_USER = lambda username: (AppiumBy.XPATH, f"//android.widget.TextView[@text='Hello, {username}']")
HELLO_USER_PT = lambda username: (AppiumBy.XPATH, f"//android.widget.TextView[@text='Olá, {username}']")

# Navigation elements
PREFERENCES_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Preferences")
MORE_OPTIONS_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "More options")
ADD_PACKAGE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Add package")

# Package related elements
PACKAGE_CODE_FIELD = (AppiumBy.ID, "br.com.muambator.android:id/package_form_text_code")
PACKAGE_NAME_FIELD = (AppiumBy.ID, "br.com.muambator.android:id/package_form_text_name")
CONFIRM_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Confirm")
PACKAGE_ITEM = lambda package_name: (AppiumBy.XPATH, f"//android.widget.TextView[@text=\"{package_name}\"]")
DELETE_OPTION = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id=\"br.com.muambator.android:id/title\" and @text=\"Delete\"]")

# Advertisement elements
SKIP_VIDEO_BUTTON = (AppiumBy.XPATH, "//android.widget.TextView[@text='Skip video']")
CLOSE_BUTTON = (AppiumBy.CLASS_NAME, "android.widget.Button")

# Error and dialog elements
ERROR_MESSAGE = (AppiumBy.ID, "android:id/message")
ERROR_CLOSE_BUTTON = (AppiumBy.ID, "android:id/button1")
ALERT_TITLE = (AppiumBy.ID, "br.com.muambator.android:id/alertTitle")

# Status elements
PENDING_BUTTON = (AppiumBy.CLASS_NAME, "android.widget.Button")
PENDING_LAYOUT = (AppiumBy.XPATH, "//android.widget.LinearLayout[@content-desc='Pending']")

# Additional elements
LOGIN_PAGE = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"Login\"]")
NEW_ACCOUNT_BUTTON = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"Nova conta\"]")
SNACKBAR_TEXT = (AppiumBy.ID, "br.com.muambator.android:id/snackbar_text")

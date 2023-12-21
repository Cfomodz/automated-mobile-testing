from appium.webdriver.common.by import By as AppiumBy

# Elementos Mapeados

# Elementos relacionados ao login
LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text=\"Faça login!\"]")
USERNAME_FIELD = (AppiumBy.ID, "br.com.muambator.android:id/username_input")
PASSWORD_FIELD = (AppiumBy.ID, "br.com.muambator.android:id/password_input")
LOGIN_CONFIRM_BUTTON = (AppiumBy.ID, "br.com.muambator.android:id/login_confirm")

# Elementos relacionados à navegação entre as abas
PENDENTES_TAB = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"PENDENTES\"]")
ENTREGUES_TAB = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"ENTREGUES\"]")
ARQUIVADOS_TAB = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"ARQUIVADOS\"]")
TRIBUTADOS_TAB = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"TRIBUTADOS\"]")

# Elementos relacionados à navegação no aplicativo
LOGO_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Logotipo Muambator")
PREFERENCES_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Preferências")
ADD_PACKAGE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Incluir pacote")

# Elementos relacionados à inclusão de pacote
PAGE_TITLE = (AppiumBy.ID, "br.com.muambator.android:id/toolbar_title")
PACKAGE_CODE_FIELD = (AppiumBy.XPATH, "//android.widget.EditText[@resource-id='br.com.muambator.android:id/package_form_text_code']")
PACKAGE_NAME_FIELD = (AppiumBy.ID, "br.com.muambator.android:id/package_form_text_name")
CONFIRM_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Confirmar")

# Elementos relacionados à interação com a publicidade
SKIP_VIDEO_BUTTON = (AppiumBy.XPATH, "//android.widget.TextView[@text=\"Pular vídeo\"]")
CLOSE_BUTTON_AFTER_SKIP = (AppiumBy.CLASS_NAME, "android.widget.Button")

# Elementos relacionados ao tratamento de erro
ERROR_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Erro")
ERROR_TEXT_ELEMENT = (AppiumBy.ID, "br.com.muambator.android:id/textinput_error")

# Elementos adicionais
USERNAME_FIELD = (AppiumBy.ID, "br.com.muambator.android:id/username_input")
PASSWORD_FIELD = (AppiumBy.ID, "br.com.muambator.android:id/password_input")
CLOSE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Navegar para cima")
ERROR_MESSAGE_ELEMENT = (AppiumBy.XPATH, "//android.widget.TextView[@text='Erro']")

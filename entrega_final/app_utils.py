from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AppUtils:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username, password):
        """Realiza o login no aplicativo."""
        el_botao_login = self.driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Button[@text=\"Faça login!\"]")
        el_botao_login.click()

        el_usuario = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_username")
        el_usuario.click()
        el_usuario.send_keys(username)

        el_senha = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_password")
        el_senha.click()
        el_senha.send_keys(password)

        el_login_confirmar = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_confirm")
        el_login_confirmar.click()

    def navigate_to_preferences(self):
        """Navega para a tela de Preferências."""
        print("Navegando para Preferências")
        el_preferencias = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Preferências"))
        )
        el_preferencias.click()

    def logout(self):
        """Realiza o logout do aplicativo."""
        print("Realizando Logout")
        el_ola_usuario = self.driver.find_element(by=AppiumBy.XPATH, value="//android.widget.TextView[@text=\"Olá, lfsdias\"]")
        el_ola_usuario.click()

        # Verifica e valida mensagem
        el_mensagem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((AppiumBy.ID, "android:id/message"))
        )

        mensagem = el_mensagem.text
        assert mensagem == "Deseja realmente sair da sua conta?", "Mensagem 'Deseja realmente sair da sua conta?' não encontrada"

        # Clique para Sair
        print("Clicando no botão de logout")
        el_logout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ID, "android:id/button1"))
        )
        el_logout.click()

    def close_error_message(self):
        """Fecha a janela de mensagem de erro."""
        try:
            print("Esperando a mensagem de erro aparecer")
            el_error_message = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.ID, "android:id/message"))
            )

            mensagem = el_error_message.text
            print(f"Mensagem de erro encontrada: {mensagem}")

            print("Clicando na mensagem de erro para fechar")
            el_error_message.click()

            # Clicar no botão para fechar a janela de mensagem
            print("Esperando o botão de fechar aparecer")
            el_close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.ID, "android:id/button1"))
            )
            print("Clicando no botão de fechar")
            el_close_button.click()
        except TimeoutException:
            print("Timeout ao tentar fechar a mensagem de erro. Verifique se o elemento está presente na página.")
            raise

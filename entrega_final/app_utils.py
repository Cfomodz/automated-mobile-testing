from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

class AppUtils:
    def __init__(self, driver):
        self.driver = driver

    def debug_print(self, message):
        if getattr(self, 'debug', False):
            print(f"DEBUG: {message}")

    def login(self, username, password):
        """Realiza o login no aplicativo."""
        # Localiza e clica no botão de login
        el_botao_login = self.driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Button[@text=\"Faça login!\"]")
        el_botao_login.click()

        # Preenche o campo de usuário
        el_usuario = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_username")
        el_usuario.click()
        el_usuario.send_keys(username)

        # Preenche o campo de senha
        el_senha = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_password")
        el_senha.click()
        el_senha.send_keys(password)

        # Confirma o login
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

        # Verifica e valida a mensagem antes de prosseguir
        el_mensagem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((AppiumBy.ID, "android:id/message"))
        )

        mensagem = el_mensagem.text
        assert mensagem == "Deseja realmente sair da sua conta?", "Mensagem 'Deseja realmente sair da sua conta?' não encontrada"

        # Clica para confirmar o logout
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

            # Clica no botão para fechar a janela de mensagem
            print("Esperando o botão de fechar aparecer")
            el_close_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.ID, "android:id/button1"))
            )
            print("Clicando no botão de fechar")
            el_close_button.click()
        except TimeoutException:
            print("Timeout ao tentar fechar a mensagem de erro. Verifique se o elemento está presente na página.")
            raise

    def add_new_packet(self, package_code, package_name):
        """Inclui um novo pacote."""

        # Clica no botão "Incluir pacote"
        el_add_package = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Incluir pacote"))
        )
        el_add_package.click()

        # Preenche o código do pacote
        el_code = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/package_form_text_code")
        el_code.click()
        el_code.send_keys(package_code)

        # Preenche o nome do pacote
        el_name = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/package_form_text_name")
        el_name.click()
        el_name.send_keys(package_name)

        # Confirma a inclusão
        el_confirm = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Confirmar")
        el_confirm.click()

        # Aguarda a inclusão ser processada
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((AppiumBy.XPATH, "//android.view.View[@resource-id=\"mys-content\"]/android.view.View[2]/android.widget.TextView"))
        ).click()

    def interact_with_advertisement(self):
        """Interage com a publicidade, se presente."""
        try:
            # Aguardar a exibição da página de publicidade
            el_advertisement = WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH,
                                                "//android.view.View[@resource-id=\"mys-content\"]/android.view.View[2]/android.widget.TextView"))
            )

            # Verificar se o elemento está presente antes de clicar
            if el_advertisement.is_displayed():
                el_advertisement.click()

                # Tentar clicar em "Pular vídeo" ou no ícone de fechar
                possible_elements = [
                    {"locator": (By.XPATH, "//android.widget.TextView[@text=\"Pular vídeo\"]"), "name": "Pular vídeo"},
                    {"locator": (By.XPATH,
                                 "//android.view.View[@resource-id=\"mys-content\"]/android.view.View[2]/android.widget.TextView"),
                     "name": "Ícone de Fechar"}
                ]

                for element_info in possible_elements:
                    try:
                        element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable(element_info["locator"])
                        )
                        element.click()
                        print(f"Clicou em {element_info['name']}")
                        break  # Se clicou em algum elemento, sair do loop
                    except TimeoutException:
                        print(f"Elemento {element_info['name']} não encontrado ou não é clicável.")

        except TimeoutException:
            # Tratar a exceção e continuar ou sinalizar uma falha, conforme necessário
            print("Elemento de publicidade não encontrado após 60 segundos.")
        except NoSuchElementException:
            # Tratar a exceção e continuar ou sinalizar uma falha, conforme necessário
            print("Elementos da publicidade não encontrados ou ações não foram necessárias")

    def delete_package(self, package_name):
        """Exclui um pacote."""
        try:
            # Verifica se o pacote está na lista antes de prosseguir
            el_package = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.XPATH,
                                            f"//android.widget.TextView[@text='{package_name}']"))
            )
            # Se o pacote estiver visível, continua com a exclusão
            el_package.click()

            # Clica no ícone "Mais opções"
            el_more_options = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Mais opções"))
            )
            el_more_options.click()

            # Escolhe a opção "Excluir"
            el_delete_option = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((AppiumBy.XPATH,
                                            "//android.widget.TextView[@resource-id=\"br.com.muambator.android:id/title\" and @text=\"Excluir\"]"))
            )
            el_delete_option.click()

            # Aguarda a tela de confirmação de exclusão
            el_confirm_title = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((AppiumBy.ID, "br.com.muambator.android:id/alertTitle"))
            )

            # Clica no botão "Confirmar"
            el_confirm_button = self.driver.find_element(by=AppiumBy.ID, value="android:id/button1")
            el_confirm_button.click()

            # Aguarda alguns segundos para a exclusão ser processada
            time.sleep(5)

        except TimeoutException:
            print(f"Pacote '{package_name}' não encontrado na lista para exclusão. Verifique se o pacote existe.")

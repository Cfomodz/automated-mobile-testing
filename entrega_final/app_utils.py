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
            # Verifique se o botão "Pular Vídeo" está presente
            try:
                el_pular_video = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((AppiumBy.XPATH, "//android.widget.TextView[@text='Pular vídeo']"))
                )
                el_pular_video.click()

                # Botão "Pular Vídeo" encontrado, aguarde mais 5 segundos para o botão de fechar aparecer
                time.sleep(5)

                # Tente clicar no botão Fechar após esperar 5 segundos
                try:
                    el_fechar = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.Button"))
                    )
                    el_fechar.click()

                except TimeoutException:
                    print("Botão de fechar não encontrado após 5 segundos.")

            except TimeoutException:
                # Botão "Pular Vídeo" não encontrado, tente clicar no botão de fechar diretamente
                try:
                    el_fechar_direto = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.Button"))
                    )
                    el_fechar_direto.click()

                except TimeoutException:
                    print("Botão de fechar não encontrado após 5 segundos.")

        except NoSuchElementException:
            # Tratar a exceção e continuar ou sinalizar uma falha, conforme necessário
            print("Elementos da publicidade não encontrados ou ações não foram necessárias")

    def verify_advertisement_screen_closed(self):
        """Verifica se a tela de publicidade foi fechada corretamente."""
        try:
            # Aguarde até 10 segundos para um elemento que indica que a tela de publicidade foi fechada
            el_advertisement_closed = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.Button"))
            )

            # Verifique se o elemento está visível
            if el_advertisement_closed.is_displayed():
                self.debug_print("A tela de publicidade foi fechada corretamente.")
                # Clique no botão "Fechar" se estiver visível
                el_advertisement_closed.click()
            else:
                self.debug_print("A tela de publicidade não foi fechada corretamente.")
        except TimeoutException:
            # Manipule a exceção conforme necessário ou sinalize uma falha
            self.debug_print("Timeout ao verificar o fechamento da tela de publicidade.")

    def delete_package(self, package_name):
        """Exclui um pacote."""
        try:
            # Verifica se o pacote está na lista antes de prosseguir
            el_package = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.XPATH,
                                            f"//android.widget.TextView[@text='{package_name}']"))
            )
            # Se o pacote estiver visível, continua com a exclusão
            el_package.click()

            # Clica no ícone "Mais opções"
            el_more_options = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Mais opções"))
            )
            el_more_options.click()

            # Escolhe a opção "Excluir"
            el_delete_option = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((AppiumBy.XPATH,
                                            "//android.widget.TextView[@resource-id=\"br.com.muambator.android:id/title\" and @text=\"Excluir\"]"))
            )
            el_delete_option.click()

            # Aguarda a tela de confirmação de exclusão
            el_confirm_title = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((AppiumBy.ID, "br.com.muambator.android:id/alertTitle"))
            )

            # Clica no botão "Confirmar"
            el_confirm_button = self.driver.find_element(by=AppiumBy.ID, value="android:id/button1")
            el_confirm_button.click()

            # Aguarda alguns segundos para a exclusão ser processada
            time.sleep(5)

        except TimeoutException:
            print(f"Pacote '{package_name}' não encontrado na lista para exclusão. Verifique se o pacote existe.")

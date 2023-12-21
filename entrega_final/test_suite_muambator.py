import pdb
import unittest
import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from app_utils import AppUtils


class TestMuambatorApp(unittest.TestCase):

    def setUp(self):
        # Configurar as capacidades desejadas do Appium
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

        # Inicializar o driver do Appium
        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        self.driver.implicitly_wait(10)  # Adiciona um wait implícito de 10 segundos

        # Inicializar a classe de utilitário
        self.app_utils = AppUtils(self.driver)

    def tearDown(self):
        # Fechar o driver do Appium após o teste
        self.driver.quit()

    def debug_print(self, message):
        if hasattr(self, 'debug') and self.debug:
            print(f"DEBUG: {message}")

    def test_login_sucess(self):
        """Testa o login com sucesso e navegação para a tela de Preferências."""
        self.debug = True

        # Dados do Login
        username = "lfsdias"
        password = "teste123"

        # Realiza o Login
        self.app_utils.login(username, password)

        # Navega para a tela de preferências
        self.app_utils.navigate_to_preferences()

        # Verifica o nome do usuário na tela "Preferências"
        self.debug_print("Verifica nome do usuário logado na tela de Preferências")
        el_ola_usuario = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((AppiumBy.XPATH, f"//android.widget.TextView[@text='Olá, {username}']"))
        )
        self.assertTrue(el_ola_usuario.is_displayed(), "Usuário não identificado na tela de Preferências")

    def test_failure_login_invalid_password(self):
        """Testa o login com falha devido à senha inválida."""
        self.debug = True

        # Dados do Login
        username = "lfsdias"
        password = "senha incorreta"

        # Realiza o Login
        self.app_utils.login(username, password)

        # Fecha a janela da mensagem de erro
        self.app_utils.close_error_message()

        # Verifica se a mensagem de erro foi fechada corretamente
        self.debug_print("Verificando se a mensagem de erro foi fechada corretamente")
        el_page_login = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text=\"Login\"]"))
        )
        self.assertTrue(el_page_login.is_displayed(), "A mensagem de erro não foi fechada corretamente")

    def test_failure_login_invalid_username(self):
        """Testa o login com falha devido à usuário inválido."""
        self.debug = True

        # Dados do Login
        username = "Kx9"
        password = "teste123"

        # Realiza o Login
        self.app_utils.login(username, password)

        # Fecha a janela da mensagem de erro
        self.app_utils.close_error_message()

        # Verifica se a mensagem de erro foi fechada corretamente
        self.debug_print("Verificando se a mensagem de erro foi fechada corretamente")
        el_page_login = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text=\"Login\"]"))
        )
        self.assertTrue(el_page_login.is_displayed(), "A mensagem de erro não foi fechada corretamente")

    def test_logout_sucess(self):
        """Testa o logout e retorno para a tela inicial."""
        self.debug = True
        # Dados do Login
        username = "lfsdias"
        password = "teste123"

        # Realiza o Login
        self.app_utils.login(username, password)
        # Navega para a tela de preferências
        self.app_utils.navigate_to_preferences()
        # Chama a função de logout
        self.app_utils.logout(username)

        # Verifica se volta para tela inicial
        self.debug_print("Verificando se retornou para a tela inicial após o logout")
        el_botao_login_apos_logout = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text=\"Nova conta\"]"))
        )
        self.assertTrue(el_botao_login_apos_logout.is_displayed(), "Não retornou para a tela inicial após o logout")

    def test_add_new_package_success(self):
        """Testa a inclusão de um novo pacote com sucesso."""
        self.debug = True

        # Dados do Login e pacote
        username = "lfsdias"
        password = "teste123"
        package_code = "OV274368708AD"
        package_name = "Pacote Automatizad3"

        # Realiza o Login
        self.app_utils.login(username, password)

        # Incluir pacote
        self.debug_print("Inclui pacote")
        self.app_utils.add_new_package(package_code, package_name)

    def test_delete_package_pending_success(self):
        """Testa a exclusão de um pacote com sucesso."""
        self.debug = True

        # Dados do Login e pacote
        username = "lfsdias"
        password = "teste123"
        package_name_to_delete = "Pacote Automatizad1"

        # Realiza o Login
        self.app_utils.login(username, password)

        # Excluir pacote da lista de PENDENTES
        self.debug_print("Excluindo o pacote da lista PENDENTES")
        self.app_utils.delete_package_pending(package_name_to_delete)

        pdb.set_trace()
        """ 
        # Verificar se o pacote foi removido corretamente
        self.debug_print("Verificando se o pacote foi removido corretamente")
        el_deleted_package = self.driver.find_elements(by=AppiumBy.XPATH,
                                                       value=f"//android.widget.TextView[@text=\"{package_name_to_delete}\"]")
        self.assertFalse(el_deleted_package, f"Pacote {package_name_to_delete} encontrado na lista após exclusão") """

        # Verificar se a exclusão foi bem-sucedida
        el_success_message = self.driver.find_elements(by=AppiumBy.ID,
                                                       value="br.com.muambator.android:id/snackbar_text")
        # Assert que o texto da mensagem é o esperado
        expected_success_message = "Pacote '{package_name_to_delete}' excluído com sucesso."
        self.assertEqual(el_success_message[0].text, expected_success_message, "Mensagem de exclusão incorreta")


if __name__ == '__main__':
    unittest.main()

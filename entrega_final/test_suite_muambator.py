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

    def test_01_login_sucess(self):
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
        self.debug_print("Verificando o nome do usuário na tela de Preferências")
        el_ola_usuario = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((AppiumBy.XPATH, f"//android.widget.TextView[@text='Olá, {username}']"))
        )
        self.assertTrue(el_ola_usuario.is_displayed(), "Nome do usuário não encontrado na tela de Preferências")

    def test_02_falha_login_senha_invalida(self):
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

    def test_03_falha_login_usuario_invalido(self):
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

    def test_04_logout_sucess(self):
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
        self.app_utils.logout()

        # Verifica se volta para tela inicial
        self.debug_print("Verificando se retornou para a tela inicial após o logout")
        el_botao_login_apos_logout = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text=\"Nova conta\"]"))
        )
        self.assertTrue(el_botao_login_apos_logout.is_displayed(), "Não retornou para a tela inicial após o logout")

    def test_05_add_new_package_success(self):
        """Testa a inclusão de um novo pacote com sucesso."""
        self.debug = True
        self.debug_print("Cenário 5: Incluir Pacote com Sucesso")

        # Dados do Login e pacote
        username = "lfsdias"
        password = "teste123"
        package_code = "NM027033020BR"
        package_name = "Pacote Automatizado"

        # Realiza o Login
        self.debug_print("Realiza Login")
        self.app_utils.login(username, password)
        time.sleep(5)

        # Incluir pacote
        self.debug_print("Inclui pacote")
        self.app_utils.add_new_packet(package_code, package_name)

        # Aguardar a exibição da página de publicidade e interagir com ela
        self.debug_print("Aguardando a exibição da página de publicidade")
        self.app_utils.interact_with_advertisement()
        time.sleep(5)  # Aguarda um tempo após interagir com a publicidade

        # Verifica se a tela de publicidade foi finalizada corretamente
        self.debug_print("Verificando se tela publicidade foi finalizada corretamente")
        self.app_utils.verify_advertisement_screen_closed()

        # Verificar se o pacote foi adicionado corretamente
        self.debug_print("Verificando se o pacote foi adicionado corretamente")
        el_added_package = self.driver.find_element(by=AppiumBy.XPATH,
                                                    value=f"//android.widget.TextView[@text=\"{package_name}\"]")
        self.assertTrue(el_added_package.is_displayed(), "Pacote não encontrado na lista")

    def test_06_delete_package_success(self):
        """Testa a exclusão de um pacote com sucesso."""
        self.debug = True
        self.debug_print("Cenário 6: Excluir Pacote com Sucesso")

        # Dados do Login e pacote
        username = "lfsdias"
        password = "teste123"
        package_name_to_delete = "Pacote Automatizado"

        # Realiza o Login
        self.debug_print("Realiza Login")
        self.app_utils.login(username, password)
        time.sleep(5)

        # Excluir pacote
        self.debug_print("Excluindo o pacote")
        self.app_utils.delete_package(package_name_to_delete)

        # Verificar se o pacote foi removido corretamente
        self.debug_print("Verificando se o pacote foi removido corretamente")
        el_deleted_package = self.driver.find_elements(by=AppiumBy.XPATH,
                                                       value=f"//android.widget.TextView[@text=\"{package_name_to_delete}\"]")
        self.assertFalse(el_deleted_package, "Pacote encontrado na lista após exclusão")


if __name__ == '__main__':
    unittest.main()

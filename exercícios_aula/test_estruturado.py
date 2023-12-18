import unittest
import time

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TesteMuambatorApp(unittest.TestCase):

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

    def tearDown(self):
        # Fechar o driver do Appium após o teste
        self.driver.quit()

    def debug_print(self, message):
        if self.debug:
            print(f"DEBUG: {message}")

    def test_login_com_sucesso_e_navegacao_para_preferencias(self):
        self.debug = True  # Altere False para não imprimir informações de depuração

        self.debug_print("Cenário 1: Login")

        # Realizar as etapas de login
        self.debug_print("Clicando no botão de login")
        el_botao_login = self.driver.find_element(by=AppiumBy.XPATH,
                                                  value="//android.widget.Button[@text=\"Faça login!\"]")
        el_botao_login.click()

        el_usuario = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_username")
        el_usuario.click()
        el_usuario.send_keys("lfsdias")

        el_senha = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_password")
        el_senha.click()
        el_senha.send_keys("teste123")

        el_login_confirmar = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_confirm")
        el_login_confirmar.click()

        # Navegar para Preferências
        self.debug_print("Navegando para Preferências")
        el_preferencias = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Preferências")
        el_preferencias.click()

        # Verificar o nome do usuário na tela "Preferências"
        self.debug_print("Verificando o nome do usuário na tela de Preferências")
        el_ola_usuario = self.driver.find_element(by=AppiumBy.XPATH,
                                                  value="//android.widget.TextView[@text=\"Olá, lfsdias\"]")
        self.assertTrue(el_ola_usuario.is_displayed(), "Nome do usuário não encontrado na tela de Preferências")
    def test_logout_e_retorno_para_tela_inicial(self):
        self.debug = True
        self.debug_print("Cenário 2: Logout")

        # Realizar as etapas de login
        self.debug_print("Clicando no botão de login")
        el_botao_login = self.driver.find_element(by=AppiumBy.XPATH,
                                                  value="//android.widget.Button[@text=\"Faça login!\"]")
        el_botao_login.click()

        el_usuario = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_username")
        el_usuario.click()
        el_usuario.send_keys("lfsdias")

        el_senha = self.driver.find_element(by=AppiumBy.ID, value="br.com.muambator.android:id/login_password")
        el_senha.click()
        el_senha.send_keys("teste123")

        el_login_confirmar = self.driver.find_element(by=AppiumBy.ID,
                                                      value="br.com.muambator.android:id/login_confirm")
        el_login_confirmar.click()

        # Navegar para Preferências
        self.debug_print("Navegando para Preferências")
        el_preferencias = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Preferências")
        el_preferencias.click()

        # Verificar o nome do usuário na tela "Preferências"
        self.debug_print("Verificando o nome do usuário na tela de Preferências")
        el_ola_usuario = self.driver.find_element(by=AppiumBy.XPATH,
                                                  value="//android.widget.TextView[@text=\"Olá, leonardoodias\"]")
        self.assertTrue(el_ola_usuario.is_displayed(), "Nome do usuário não encontrado na tela de Preferências")
        el_ola_usuario.click()

        # Verificar mensagem e validar
        el_mensagem = self.driver.find_element(by=AppiumBy.ID, value="android:id/message")
        self.assertTrue(el_mensagem.is_displayed(), "Mensagem 'Deseja realmente sair da sua conta?' não encontrada")
        mensagem = el_mensagem.text
        self.assertEqual(mensagem, "Deseja realmente sair da sua conta?")

        # Clique para Sair
        self.debug_print("Clicando no botão de logout")
        el_logout = self.driver.find_element(by=AppiumBy.ID, value="android:id/button1")
        self.debug_print("Esperando até que o botão de logout seja clicável")
        el_logout = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "android:id/button1"))
        )
        el_logout.click()

        # Verifica se volta para tela inicial
        self.debug_print("Verificando se retornou para a tela inicial após o logout")
        el_botao_login_apos_logout = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//android.widget.TextView[@text=\"Nova conta\"]"))
        )
        self.assertTrue(el_botao_login_apos_logout.is_displayed(), "Não retornou para a tela inicial após o logout")


if __name__ == '__main__':
    unittest.main()

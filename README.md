# Projeto de Testes Automatizados - Muambator 🚀

- Avaliação do curso de Especialização em Testes Ageis (ETA) da Cesar School para a disciplina Tópicos especiais II (Testes Mobile). 
- Professor Samuel Elias Bravo Lopez 
- Aluno: Leonardo Felipe da Silva Dias

## Descrição do Projeto
Este projeto visa automatizar testes no aplicativo Muambator, utilizando Python, Appium, e Vysor.

- **Muambator:** Aplicativo para rastreamento de encomendas, proporcionando uma forma inteligente e prática de monitorar pacotes postados nos Correios e outras empresas.

## Tecnologias Utilizadas
- **Python:** Linguagem principal do projeto.
- **Appium:** Framework de automação para testes mobile.
- **Unittest:** Framework de testes unitários em Python.
- **ADB (Android Debug Bridge):** Ferramenta para interação com dispositivos Android.
- **Selenium**

## Estrutura do Projeto
O projeto segue a arquitetura de Page Object Model (POM) para uma organização mais eficiente e manutenção dos testes.
O projeto segue a seguinte estrutura:

- **`app_utils.py`:** Classe utilitária para interações com o aplicativo.
- **`test_suite_muambator.py`:** Arquivo contendo os métodos/funções de teste.
- **`requirements.txt`:** Lista de dependências do projeto.

## Pré-requisitos
- Certifique-se de atender aos seguintes pré-requisitos antes de executar os testes:

- Editor de codigo (Visual Studio Code) ou uma IDE (Pycharm)
- Python 3.x instalado
- Appium configurado
- Android SDK instalado ou Android Studio para obter o ADB
- Dispositivo Android conectado e Vysor ou emulador configurado
- ADB configurado e acessível pelo terminal
- Bibliotecas Python instaladas (verificar o arquivo requirements.txt)
- Conta válida no Muambator para execução dos testes
- Massa de Teste: [Códigos de Rastreio](https://linketrack.com/?utm_source=navbar)

## Configuração do Ambiente e Instruções para Execução

1. **Python e Dependências:**
   - Instale o Python em seu sistema.
   - Instale as dependências usando o comando:
     ```
     pip install -r requirements.txt
     ```
2. **Appium e Configurações:**
   - Instale o Appium em sua máquina.
   - Configure as capacidades necessárias no arquivo de configuração do Appium.
   - Inicie o Appium Server.

3. **ADB (Android Debug Bridge):**
   - Instale o Android SDK ou Android Studio para obter o ADB.
   - Certifique-se de que o ADB esteja disponível no seu PATH.

     ```bash
     python test_suite_muambator.py
     ```

## Execução dos Testes
- Execute os testes usando o seguinte comando:

     ```bash
     python test_suite_muambator.py
     ```
  
## Observações
- Mantenha uma conta válida no Muambator, pois as funcionalidades requerem autenticação.

## Referências
- [Muambator](https://www.muambator.com.br/): Saiba mais sobre o aplicativo Muambator. Assita o vídeo também https://www.youtube.com/watch?v=6AhPVfRkJBs
- [Appium](http://appium.io/): Documentação oficial do Appium.
- [Vysor](https://www.vysor.io/): Página oficial do Vysor.
- [ADB (Android Debug Bridge)](https://developer.android.com/studio/command-line/adb): Documentação oficial do ADB.
- Sites de download de APK: 1- https://apps.evozi.com/apk-downloader/  2- https://apkpure.com/


from time import sleep
from random import uniform
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from modules.utils.general import DotEnv
from core.logger import Logger

class SeleniumElement:
    """
    Classe utilitária para facilitar a busca robusta e a interação com elementos web
    usando Selenium WebDriver.

    Inclui esperas explícitas (WebDriverWait) e a capacidade de procurar elementos
    dentro de iframes aninhados.
    """

    __BY_MAP = {
        "id": By.ID,
        "xpath": By.XPATH,
        "name": By.NAME,
        "css": By.CSS_SELECTOR,
        "class": By.CLASS_NAME,
        "tag": By.TAG_NAME
    }


    def __init__(self, driver, by, value, timeout=2):
        """
        Inicializa o objeto SeleniumElement com o contexto de busca.

        Args:
            driver (WebDriver | WebElement): A instância do Selenium WebDriver ou um
                WebElement (para buscas aninhadas).
            by (str): O tipo de busca (ex: "id", "xpath", "css", "class", "name", "tag").
            value (str): O valor a ser buscado (ex: o ID, a expressão XPath).
            timeout (int, optional): O tempo máximo de espera em segundos para encontrar
                o elemento. Padrão é 2.
        """
        self.__driver = driver
        self.__by = by
        self.__value = value
        self.__timeout = timeout


    def find(self, context=None):
        """
        Procura por um **único elemento** na página atual.

        Utiliza EC.visibility_of_element_located para garantir que o elemento esteja
        visível. Se não for encontrado no contexto principal, itera sobre todos os
        iframes presentes, alternando o contexto, para tentar localizar o elemento.

        Raises:
            TimeoutException: Se o elemento não for encontrado após o timeout em
                nenhum contexto (principal ou iframes).

        Returns:
            WebElement: O elemento Selenium encontrado.
        """

        # Faz a busca da propriedade By com base no valor fornecido no construtor
        by = self.__BY_MAP.get(self.__by.lower(), self.__by)
        driver = context or self.__driver
        # Tenta encontrar o elemento no contexto atual
        
        try:
            if isinstance(driver, WebDriver):
                # tenta achar o elemento usando espera explicita para visibilidade
                element = WebDriverWait(driver, self.__timeout).until(
                    EC.visibility_of_element_located((by, self.__value))
                )

            else:
                # tenta achar o elemento diretamente no WebElement fornecido
                element = self.__driver.find_element(by, self.__value)

            return element

        except:
            pass

        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            driver.switch_to.frame(iframe)
            try:
                element = self.find(context=driver)
                if element:
                    return element
            except:
                pass
            
            driver.switch_to.parent_frame()

        #return False
        raise Exception(f"Elemento '{self.__value}' não encontrado.")

    
    def find_many(self, context=None):
        """
        Procura por **múltiplos elementos** na página.

        Utiliza EC.presence_of_all_elements_located. Busca elementos no contexto
        principal e recursivamente em todos os iframes encontrados.

        Raises:
            TimeoutException: Se nenhum elemento for encontrado no contexto principal
                ou em qualquer iframe.

        Returns:
            list[WebElement]: Uma lista de elementos Selenium encontrados.
        """

        by = self.__BY_MAP.get(self.__by.lower(), self.__by)

        driver = self.__driver
        root = context or driver
        elements_found = []

        try:
            if isinstance(root, WebDriver):
                elements = WebDriverWait(driver, self.__timeout).until(
                    EC.presence_of_all_elements_located((by, self.__value))
                )
            else:
                elements = root.find_elements(by, self.__value)

            elements_found.extend(elements)

        except:
            pass

        iframes = root.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            driver.switch_to.frame(iframe)

            try:
                elements = self.find_many(context=driver)
                if elements:
                    elements_found.extend(elements)
            except:
                pass

            driver.switch_to.parent_frame()

        return elements_found
    
   
    def find_error_msg(self):
        """
        Procura por um único elemento utilizando EC.presence_of_element_located.

        É útil para localizar elementos que existem no DOM (como mensagens de erro
        escondidas), mas podem não estar visíveis. Inclui a mesma lógica de
        busca em iframes que o método find().

        Raises:
            TimeoutException: Se o elemento não for encontrado em nenhum contexto.

        Returns:
            WebElement: O elemento Selenium encontrado.
        """
        # Faz a busca da propriedade By com base no valor fornecido no construtor
        by = self.__BY_MAP.get(self.__by.lower(), self.__by)
        
        # Tenta encontrar o elemento no contexto atual
        try: 
            if isinstance(self.__driver, WebDriver):
                # then find the element using explicit wait for presence
                element = WebDriverWait(self.__driver, self.__timeout).until(
                    EC.presence_of_element_located((by, self.__value))
                )

            else:
                element = self.__driver.find_element(by, self.__value)

            return element

        except TimeoutException:
            pass

        iframes = self.__driver.find_elements(By.TAG_NAME, "iframe")

        for iframe in iframes:
            self.__driver.switch_to.frame(iframe)

            try:

                self.__timeout = 0  # evita espera desnecessária em iframes aninhados

                element = self.find()

                if element:
                    self.__driver.switch_to.default_content() # Volta ao contexto principal antes de retornar
                    return element
            
            except TimeoutException:
                self.__driver.switch_to.parent_frame()
                pass

        self.__driver.switch_to.default_content()
        # Se chegou aqui, não encontrou em lugar nenhum
        raise TimeoutException(f"A o elemento: '{self.__value}' não foi encontrado em nenhum iframe..")


    def action(self, action, text=None):
        """
        Encontra o elemento e executa uma ação especificada nele.

        As ações suportadas são: "click", "write", "press", "move_to" e "void".

        Args:
            action (str): A ação a ser realizada (ex: "click", "write").
            text (str, optional): O texto a ser usado para as ações "write" ou "press"
                (ex: uma string ou uma Key do Selenium como "Keys.ENTER").

        Ações Especiais:
            - "write": Limpa o campo, clica e digita o texto com um delay aleatório
              entre caracteres para simular digitação humana.
            - "move_to": Move o cursor do mouse para o elemento.

        Returns:
            bool: True em caso de sucesso na execução da ação, False em caso de falha.
        """

        element = self.find()

        if element is None:
            print("Element not found, cannot perform action.")
            return False
        
        action = action.lower().strip()
        
        try:
            if action == "click":
                element.click()

            elif action == "write" and text is not None:
                
                element.clear()
                sleep(0.5)
                element.click()

                for char in text:
                    element.send_keys(char)
                    sleep(uniform(0.03, 0.05))

            elif action == "press" and text is not None:
                element.send_keys(text)

            elif action == "void":
                return ""
            
            elif action == "move_to":
                actions = ActionChains(self.__driver)
                actions.move_to_element(element).perform()
            
            else:
                print(f"Unsupported action: {action}")
                return False
            
            return True
        except Exception as e:
            print(f"Error performing {action} on element: {e}")
            return False
        
        finally:
            # Nota: O retorno para default_content() foi movido para os metodos find()
            # para garantir que o contexto seja resetado corretamente apos a busca.
            pass

class SeleniumBrowserOptions:
    """
    Classe para configurar opções e serviços para a inicialização do Selenium WebDriver.
    Atualmente suporta apenas a configuração do Chrome.
    """
    def __init__(self):
        pass

    def chrome(self):
        """
        Configura e retorna as opções (Options) e o serviço (Service)
        necessários para iniciar uma instância do Chrome WebDriver.

        As opções configuradas visam otimizar a automação e evitar a detecção:
        - Inicia maximizado.
        - Desabilita notificações, barras de informação, extensões e popups.
        - Configura switches experimentais para exclusão de automação e logs.
        - Argumentos de estabilidade: --no-sandbox, --disable-dev-shm-usage.

        Returns:
            tuple[Options, Service]: Uma tupla contendo (options, service) do Chrome.
        """
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")  
        if DotEnv().get('DOCKER_RUNNING').lower() == "true":
            options.add_argument("--headless=new")
            options.add_experimental_option("useAutomationExtension", False)

        service = Service(ChromeDriverManager().install())

        return options, service

class BrowserAutomation:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        # service = Service()  # Usa o ChromeDriver padrão no PATH
        options, service = SeleniumBrowserOptions().chrome()
        self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver  # Retorna o driver para uso dentro do 'with'

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
            return True
        # Retorne False para propagar exceções, True para suprimir
        return False
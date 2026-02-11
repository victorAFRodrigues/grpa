from selenium import webdriver
from core.browser_automation import SeleniumBrowserOptions as SBO

class Automation:
    def __init__(self):
        self.driver = None

    def __enter__(self):
        # service = Service()  # Usa o ChromeDriver padrão no PATH
        options, service = SBO().chrome()
        self.driver = webdriver.Chrome(service=service, options=options)
        return self.driver  # Retorna o driver para uso dentro do 'with'

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
            return True
        # Retorne False para propagar exceções, True para suprimir
        return False

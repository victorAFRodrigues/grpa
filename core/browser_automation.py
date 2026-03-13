from datetime import datetime
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


class PlaywrightElement:
    """
    Classe utilitária para busca robusta e interação com elementos
    usando Playwright, incluindo suporte a iframes aninhados.
    """

    def __init__(self, page, selector: str, timeout: int = 2000):
        self.page = page
        self.selector = selector
        self.timeout = timeout

    # ===============================
    # Busca recursiva em frames
    # ===============================
    def _find_in_frame(self):
        for frame in self.page.frames:
            locator = frame.locator(self.selector)
            if locator.count():
                return locator.first

        return None

    # ===============================
    # Encontrar um único elemento
    # ===============================
    def find(self):
        try:
            locator = self.page.locator(self.selector)
            locator.first.wait_for(timeout=self.timeout)
            return locator.first
        except PlaywrightTimeoutError:
            pass

        el = self._find_in_frame()

        if el:
            return el

        print(f"Elemento '{self.selector}' não encontrado.")
        raise Exception(f"Elemento '{self.selector}' não encontrado.")

    # ===============================
    # Encontrar múltiplos elementos
    # ===============================
    def find_many(self):
        for frame in self.page.frames:
            locator = frame.locator(self.selector)
            if locator.count() > 0:
                return locator
        return None

    # ===============================
    # Encontrar elemento presente (não precisa estar visível)
    # ===============================
    def find_error_msg(self):
        for frame in self.page.frames:
            locator = frame.locator(self.selector)
            if locator.count() > 0:
                return locator.first

        raise Exception(f"Elemento '{self.selector}' não encontrado em nenhum iframe.")

    # ===============================
    # Ações
    # ===============================
    def action(self, action: str, text: str = None):
        element = self.find()

        action = action.lower().strip()

        try:
            if action == "click":
                element.click()

            elif action == "write" and text is not None:
                # element.fill("")
                # sleep(0.2)
                #
                # for char in text:
                #     element.type(char, delay=uniform(30, 50))

                element.fill(text)

            elif action == "press" and text is not None:
                element.press(text)

            elif action == "move_to":
                element.hover()

            elif action == "void":
                return ""

            else:
                print(f"Ação não suportada: {action}")
                return False

            return True

        except Exception as e:
            print(f"Erro executando {action} no elemento: {e}")
            return False

    # ===============================
    # Screenshot
    # ===============================
    @staticmethod
    def screenshot(page):
        ROOT_DIR = Path(__file__).resolve().parent.parent
        SCREENSHOT_DIR = ROOT_DIR / "screenshots"
        SCREENSHOT_DIR.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = SCREENSHOT_DIR / f"screenshot_{timestamp}.png"

        page.screenshot(
            path=str(filename),
            full_page=True
        )


# =======================
# Browser Configuration
# =======================
class PlaywrightBrowserOptions:

    def __init__(self):
        self.docker_running = True

        load_dotenv(find_dotenv())

        if os.getenv('ENV') != 'docker':
            self.docker_running = False

    def launch(self, playwright):
        headless =  self.docker_running
        args = [
            "--no-sandbox",
            "--disable-setuid-sandbox",

            "--disable-dev-shm-usage",
            "--disable-gpu=false",

            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-background-timer-throttling"
        ]

        if headless:
            args.append("--headless=new")

        browser = playwright.chromium.launch(
            headless=headless,
            args=args
        )

        context = browser.new_context(
            # viewport=None  # equivalente ao start-maximized
            viewport={"width": 1024, "height": 768}
        )

        return browser, context


# ================
# Context Manager
# ================
class BrowserAutomation:

    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        self.playwright = sync_playwright().start()

        self.browser, self.context = PlaywrightBrowserOptions().launch(self.playwright)

        self.page = self.context.new_page()

        return self.page  # retorna page para uso dentro do with

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            PlaywrightElement.screenshot(self.page)

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

        # Retorne False para propagar exceções
        return False

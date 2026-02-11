from modules.utils.general import ResourcePath
import threading
import os
from PIL import Image, ImageDraw
import pystray

class App:
    def __init__(self):
        self.icon_path = ResourcePath("public/icon/rpa_goevo.ico")
        self.icon = None
        self.running = True

    def _exit_callback(self):
        """
        Função chamada ao clicar em 'Sair' no ícone da bandeja.
        """
        self.running = False
        nome_executavel = "GRPA.exe"
        os.system(f"taskkill /f /im {nome_executavel}")

    def _create_tray_icon(self):
        """
        Cria o ícone da bandeja do sistema.
        """
        def on_exit(icon, item):
            icon.stop()
            self._exit_callback()

        try:
            image = Image.open(self.icon_path)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")
            # Fallback: cria ícone simples se não encontrar o arquivo
            width, height = 64, 64
            image = Image.new('RGB', (width, height), (50, 100, 150))
            dc = ImageDraw.Draw(image)
            dc.rectangle([0, 0, width, height], fill=(50, 100, 150))
            dc.text((10, 25), "RPA", fill=(255, 255, 255))

        self.icon = pystray.Icon("GOEVO RPA")
        self.icon.icon = image
        self.icon.title = "GOEVO RPA - Executando"
        self.icon.menu = pystray.Menu(
            pystray.MenuItem("Encerrar RPA", on_exit)
        )

    def start_tray(self):
        """
        Inicia o ícone da bandeja em uma thread separada.
        """
        self._create_tray_icon()
        if self.icon:
            threading.Thread(target=self.icon.run, daemon=True).start()

    # Context manager methods
    def __enter__(self):
        self.start_tray()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.icon:
            self.icon.stop()
        self.running = False
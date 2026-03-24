import requests
import zipfile
import shutil
import tempfile
from pathlib import Path

from modules.utils.general.env import DotEnv


class Updater:
    def __init__(self):
        self.dotenv = DotEnv()

    @staticmethod
    def bootstrap_automations():
        root = Path(__file__).resolve().parents[1]
        automations_dir = root / "automations"

        # se volume estiver vazio, copia automations da imagem
        if not any(automations_dir.iterdir()):
            print("Inicializando automations no volume...")

            image_automations = Path("/app/default_automations")

            shutil.copytree(image_automations, automations_dir, dirs_exist_ok=True)

    @staticmethod
    def automations(url: str):
        # pasta do projeto
        root = Path(__file__).resolve().parents[1]
        automations_dir = root / "automations"

        # cria diretório temporário
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_dir = Path(tmp_dir)
            zip_path = tmp_dir / "automations.zip"

            # baixar o zip
            response = requests.get(url, stream=True)
            response.raise_for_status()

            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # extrair o zip
            extract_dir = tmp_dir / "extracted"
            extract_dir.mkdir()

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

            # procurar pasta automations dentro do zip
            new_automations = None
            for path in extract_dir.rglob("automations"):
                if path.is_dir():
                    new_automations = path
                    break

            if not new_automations:
                raise Exception("Pasta 'automations' não encontrada no zip")

            # remover automations antiga
            if automations_dir.exists():
                shutil.rmtree(automations_dir)

            # mover nova automations
            shutil.copytree(new_automations, automations_dir)

            version = url.split("/")[-1].split('v')[-1].replace('.zip', '')

            print("Updating version:", version)

            DotEnv().set('GRPA_AUTOMATION_VERSION', version)


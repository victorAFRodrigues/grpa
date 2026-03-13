from time import time
import base64
import tempfile
import os
import sys
from dotenv import load_dotenv, find_dotenv
from core.logger import Logger

class ExecTime:
    def __init__(self, name="Bloco"):
        self.name = name

    def __enter__(self):
        self.start = time()
        return self  # permite acessar atributos depois, se quiser

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time()
        print(f"\nO tempo de execução de '{self.name}' foi: {end - self.start:.4f} segundos\n")

class Xml:
    def __init__(self, file_content, file_name):
        self.__file_content = file_content
        self.__file_name = file_name

    def generate(self):
        try:
            if not self.__file_content:
                raise Exception("Conteúdo do XML está vazio")

            base64_data = self.__file_content.replace(
                'data:text/xml;base64,',
                ''
            ).strip()

            xml_data = base64.b64decode(base64_data)

            if not xml_data:
                raise Exception("XML decodificado está vazio")

            temp_path = os.path.join(
                tempfile.gettempdir(),
                self.__file_name
            )

            with open(temp_path, "wb") as f:
                f.write(xml_data)

            return temp_path

        except Exception as e:
            raise Exception(f"Erro ao gerar XML: {e}")

class DotEnv:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.log = Logger('DotEnv').get_logger()

    def get(self, key):
        self.log.info('Capiturando variavel de ambiente...')
        value = os.getenv(key)

        if value is None:
            raise KeyError(f'A variável de ambiente "{key}" não está cadastrada.')

        self.log.info('Capiturando variavel de ambiente...')
        return value

    def set(self, key, value):
        try:
            with open(find_dotenv(), "r") as f:
                rows = f.readlines()
                print(rows)
        except FileNotFoundError:
            rows = []

        found = False
        with open(find_dotenv(), "w") as f:
            for row in rows:
                if row.startswith(f"{key}="):
                    f.write(f'{key}="{value}"\n')
                    found = True
                else:
                    f.write(row)
            if not found:
                f.write(f'{key}="{value}"\n')
           
class ResourcePath:
    """
    Classe que resolve o caminho absoluto de um recurso.
    Executa automaticamente a lógica ao ser instanciada.
    """
    def __init__(self, relative_path: str):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS  # usado pelo PyInstaller
        else:
            base_path = os.path.abspath("")
        
        # resultado final
        self.result = os.path.join(base_path, relative_path)
    
    def __str__(self):
        """Permite usar print(ResourcePath('...')) diretamente"""
        return self.result
    
    def __fspath__(self):
        """Permite usar este objeto onde um caminho de arquivo é esperado."""
        return self.result


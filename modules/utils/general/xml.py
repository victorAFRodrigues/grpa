import base64
import os
import tempfile


class Xml:
    def __init__(self, file_content, file_name):
        self.__file_content = file_content
        self.__file_name = file_name

    def generate(self):
        try:
            if not self.__file_content:
                print("Conteúdo do XML está vazio")
                raise Exception("Conteúdo do XML está vazio")

            base64_data = self.__file_content.replace(
                'data:text/xml;base64,',
                ''
            ).strip()

            xml_data = base64.b64decode(base64_data)

            if not xml_data:
                print("Conteúdo do XML está vazio")
                raise Exception("XML decodificado está vazio")

            temp_path = os.path.join(
                tempfile.gettempdir(),
                self.__file_name
            )

            with open(temp_path, "wb") as f:
                f.write(xml_data)

            return temp_path

        except Exception as e:
            print(f"Erro ao gerar XML: {e}")
            raise Exception(f"Erro ao gerar XML: {e}")


import json

from automations.dealernet.common import login
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.xml import Xml


def run(page, log, xml_path):
    try:
        PlaywrightElement(page, '//button[normalize-space()="Integração"]').action('click')
        PlaywrightElement(page, '//span[normalize-space()="XML - Importação"]', 3000).action('move_to')
        PlaywrightElement(page, '//span[normalize-space()="Nota Fiscal de Item Avulso"]').action('click')

        PlaywrightElement(page, '//*[@id="IMAGE1"]').action('click')

        PlaywrightElement(page, '//*[@id="IMAGE2"]', 3000).action('click')

        upload_input = PlaywrightElement(page, '//*[@id="uploadfiles"]', 4000)

        if upload_input.find():
            upload_input.find().set_input_files(xml_path)

        PlaywrightElement(page, '//*[@id="TRN_ENTER"]').action('click')

        msg = PlaywrightElement(page, '//*[@id="TEXTBLOCKDOWNLOAD"]/a/text', 3000).find().inner_text()

        if msg != 'Arquivos processados 1 de 1. Clique aqui para Visualizar':
            raise Exception('Arquivo invalido, cancelando execução...')

        PlaywrightElement(page, '//*[@id="TRN_CANCEL"]').action('click')

        log.succcess('Importação de NFe concluída!')

    except Exception as e:
        log.error(e)
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.common.xml_import").get_logger()

    path = f'../data/cadastrar_nf_produto.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = json.load(file)

    _xml_path = Xml(
        _data["nfexml_content"],
        _data["nfexml_filename"]
    ).generate()

    with BrowserAutomation() as _page:
        login.run(_page, _log)

        run(_page, _log, _xml_path)
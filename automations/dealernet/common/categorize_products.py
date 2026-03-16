import json
from automations.dealernet.common import login, import_xml, select_xml
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime
from modules.utils.general.xml import Xml


def run(page, log):
    try:
        PlaywrightElement(page, '#vITEMAVULSO_CODIGO', 4000).action('write', '5')
        PlaywrightElement(page, '#CONFIRM').action('click')
        PlaywrightElement(page, '#BTNCONFIRMAR').action('click')

        processing_btn = PlaywrightElement(page, '#BTNPROCESSAR', 5000).find()
        if not processing_btn.is_visible():
            raise Exception('o botão de processar não apareceu, verifique.')
        processing_btn.click()

        log.success('Categorização dos produtos da nota concluído!')

    except Exception as e:
        log.error(f"Não foi possivel preencher a capa da nota, erro: {e}")
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.common.categorize_products").get_logger()

    path = f'../data/cadastrar_nf_produto.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = json.load(file)

    _xml_path = Xml(
        _data["nfexml_content"],
        _data["nfexml_filename"]
    ).generate()

    with ExecTime(_log, 'categorize_products'):
        with BrowserAutomation() as _page:
            login.run(_page, _log)

            import_xml.run(_page, _log, _xml_path)

            select_xml.run(_page, _log, _data)

            run(_page, _log)
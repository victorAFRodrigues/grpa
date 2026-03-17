import json
from automations.dealernet.common import login, import_xml, select_xml, categorize_products, \
    fill_pre_product_invoice_cover
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime
from modules.utils.general.xml import Xml


def run(page, log, data):

    try:
        # direciona para pagina de entrada de nota (item avulso)
        PlaywrightElement(page, '//button[normalize-space()="Produtos"]').action('click')
        PlaywrightElement(page, '//span[normalize-space()="Nota Fiscal"]', 3000).action('move_to')
        PlaywrightElement(page, '//span[normalize-space()="NF Entrada Item Avulso"]').action('click')

        # preenche os filtros e efetua busca pela nota
        PlaywrightElement(page, '#vNOTAFISCAL_NUMERO').action('write', data["numero_nf"])
        select = PlaywrightElement(page, '#vNOTAFISCAL_STATUS')
        select.find().select_option('PEN')
        PlaywrightElement(page, '#IMGREFRESH').action('click')

        PlaywrightElement(page, '#GridContainerTbl', 3000).find()

        cell = PlaywrightElement(page, f'td[colindex="4"] span:has-text("{data["numero_nf"]}")').find_many()

        cell = cell.nth(0)

        button = cell.locator(
            'xpath=ancestor::tr'
        ).locator(
            'td[colindex="1"] input'
        ).first

        if button:
            button.click()
        else:
            raise Exception("Nenhuma nota 'pendente' estava disponível")

        log.success('nota selecionada, direcionando para a tela de preenchimento da capa da nota...')


    except Exception as e:
        log.error(f"Não foi possivel preencher a capa da nota, erro: {e}")
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.common.select_invoice").get_logger()

    path = f'../data/cadastro_nf_produto.json'

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

            categorize_products.run(_page, _log)

            fill_pre_product_invoice_cover.run(_page, _log, _data)

            run(_page, _log, _data)
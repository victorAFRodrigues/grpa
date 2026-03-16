from calendar import monthrange
from datetime import datetime
from json import load
from automations.dealernet.common import login, import_xml
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime


def run(page, log, data):

    today = datetime.now()
    year, month = today.year, today.month
    last_month_day = f'{monthrange(year, month)[1]:02d}/{month:02d}/{str(year)[-2:]}'
    data_emissao = data["data_emissao"]
    data_emissao = datetime.strptime(data_emissao, "%d/%m/%Y")
    data_emissao = data_emissao.strftime("%d/%m/%y")
    xml_filename = data["nfexml_filename"].replace('.xml','')
    
    try:

        PlaywrightElement(page, '#vINTEGRACAOXMLNF_DATAEMISSAOINICIAL').action('write', data_emissao)
        PlaywrightElement(page, '#vINTEGRACAOXMLNF_DATAEMISSAOFINAL').action('write', last_month_day)
        PlaywrightElement(page, '#IMAGE2').action('click')

        PlaywrightElement(page, '#GridxmlContainerTbl', 3000).find()

        cell = PlaywrightElement(page, f'td[colindex="6"] span:has-text("{xml_filename}")').find()

        button = cell.locator(
            'xpath=ancestor::tr'
        ).locator(
            'td[colindex="10"] img[title="Atualizar dados Itens Avulsos da NF"]'
        ).first

        button.click()

        log.success('XML encontrado e selecionado.')
        log.info('Direcionando para a tela de preenchimento da capa da nota...')

    except Exception as e:
        log.error(e)
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger('automation.dealernet.common.select_xml').get_logger()

    path = f'../data/cadastro_nf_produto.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'select_xml'):
        with BrowserAutomation() as _page:
            login.run(_page, _log)

            import_xml.run(_page, _log, _data)

            run(_page, _log, _data)


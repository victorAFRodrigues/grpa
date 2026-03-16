from json import load
from automations.dealernet.common import login, fill_service_invoice_cover
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime


def run(page, log, data):

    try:
        PlaywrightElement(page, '//*[@id="ITEMAVULSO"]').action('click')

        PlaywrightElement(page, '//*[@id="vNOTAFISCALITEM_ITEMAVULSOCOD"]', 4000).action('write', '12')

        PlaywrightElement(page, '//*[@id="vNOTAFISCALITEM_OBSERVACAO"]').action('write',  data['observacao'])

        PlaywrightElement(page, '//*[@id="vNOTAFISCALITEM_CONTAGERENCIALCOD"]').action('write', data['conta_gerencial'])

        select = PlaywrightElement(page, 'select[id="vNOTAFISCALITEM_DEPARTAMENTOCOD"]')
        select.find().select_option(data['rateio'][0]["departamento"])

        PlaywrightElement(page, '//*[@id="vNOTAFISCALITEM_QTDE"]').action('write', '1')

        select = PlaywrightElement(page, 'select[id="vNOTAFISCALITEM_UNIDADECOD"]')
        select.find().select_option('1')

        PlaywrightElement(page, '//*[@id="vNOTAFISCALITEM_VALORUNITARIO"]').action('write', data['valor_total'])

        PlaywrightElement(page, '//*[@id="CONFIRMAR"]').action('click')

        log.success("Item da nota cadastrado com sucesso!")
    except Exception as e:
        log.error(f"Não foi possivel cadastrar o item, erro: {e}")
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.use_cases.fill_invoice_item").get_logger()

    path = f'../data/cadastro_nf_produto.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'fill_invoice_item'):
        with BrowserAutomation() as _page:
            login.run(_page, _log, _data)

            fill_service_invoice_cover.run(_page, _log, _data)

            run(_page, _log, _data)
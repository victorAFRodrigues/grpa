from json import load
from automations.dealernet.common import login, fill_service_invoice_cover, fill_invoice_item
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime

def run(page, log, data):

    parcelas = data["parcelas"]

    if len(parcelas) < 2:
        return True

    try:
        PlaywrightElement(page, '//*[@id="RATEIO"]').action('click')

        btn_insert = PlaywrightElement(page, '//*[@id="IMGINSERT"]').find()
        btn_insert.wait_for()
        btn_insert.click()

        n = 0

        rateio = data["rateio"]

        for rateio_i in rateio:

            select = PlaywrightElement(page, 'select[id="vNOTAFISCALRATEIODEP_EMPRESACOD"]')
            select.find().select_option(rateio_i['empresa'])

            select = PlaywrightElement(page, 'select[id="vNOTAFISCALRATEIODEP_DEPARTAMENTOCOD"]')
            select.find().select_option(rateio_i['departamento'])

            select = PlaywrightElement(page, 'select[id="vCONTAGERENCIAL_CODIGO"]')
            select.find().select_option(rateio_i['conta_gerencial'])

            PlaywrightElement(page, '//*[@id="vNOTAFISCALRATEIODEP_VALOR"]').action('write',  rateio_i['valor'])
            PlaywrightElement(page, '//*[@id="CONFIRMAR"]').action('click')

            # verfica se há mais de um item para cadastrar no rateio
            if len(rateio) > 1 and n < len(rateio) - 1:
                n += 1

                # verfica se há mais de uma parcela para cadastrar
                PlaywrightElement(page, '//*[@id="IMGINSERT"]').action('click')

        PlaywrightElement(page, '//*[@id="FECHAR"]').action('click')

        log.success('Rateio cadastrado com sucesso!')

        return True

    except Exception as e:
        log.error(f"Não foi possivel realizar o rateio, erro: {e}")
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger('automation.dealernet.common.fill_cost_allocation').get_logger()

    path = f'../data/cadastrar_nf_servico.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'fill_cost_allocation'):
        with BrowserAutomation() as _page:
            login.run(_page, _log)

            fill_service_invoice_cover.run(_page, _log, _data)

            fill_invoice_item.run(_page, _log, _data)

            run(_page, _log, _data)
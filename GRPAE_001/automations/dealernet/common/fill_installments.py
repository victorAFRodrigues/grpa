from json import load
from time import sleep
from automations.dealernet.common import login, fill_service_invoice_cover, fill_invoice_item
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime

def run(page, log, data):

    parcelas = data["parcelas"]

    try:
        PlaywrightElement(page, '//*[@id="PARCELA"]', 4000).action('click')

        btn_insert = PlaywrightElement(page, '//*[@id="INSERT"]').find()
        btn_insert.wait_for()
        btn_insert.click()

        i = 0

        for parcela in parcelas:
            sleep(1)

            log.info(f"Preenchendo parcela {i + 1} de {len(parcelas)}")

            # encontra as linhas da tabela de parcelas
            rows = PlaywrightElement(page,  '//*[@id="GridparcelaContainerTbl"]/tbody/tr').find_many()

            row = rows.nth(i)
            row.locator('td[colindex="17"] div input').fill(parcela['data_vencimento'])
            row.locator('td[colindex="19"] input').fill(parcela['valor'])

            row.locator('td[colindex="20"] select').select_option(
                parcela['tipo_titulo']
            )

            # verfica se há mais de uma parcela para cadastrar
            if len(parcelas) > 1 and i < len(parcelas) - 1:
                i += 1

                # clica para inserir uma nova parcela
                PlaywrightElement(page, '//*[@id="INSERT"]').action('click')

        PlaywrightElement(page, '//*[@id="BTNCONFIRMAR"]').action('click')

        log.success('Parcelas cadastradas com sucesso!')

        return True


    except Exception as e:
        log.error(f"Não foi possivel cadastrar as parcelas: {e}")
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.common.fill_installments").get_logger()

    path = f'../data/cadastro_nf_servico.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'fill_installments'):
        with BrowserAutomation() as _page:
            login.run(_page, _log)

            fill_service_invoice_cover.run(_page, _log, _data)

            fill_invoice_item.run(_page, _log, _data)

            run(_page, _log, _data)

            sleep(5)
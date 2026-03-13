from json import load
from automations.dealernet.common import login, fill_service_invoice_cover, fill_invoice_item, fill_installments, \
    fill_cost_allocation
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime


def run(page, log, data):
    try:
        login.run(page, log, data)

        fill_service_invoice_cover.run(page, log, data)

        fill_invoice_item.run(page, log, data)

        if len(data['parcelas']) > 1:
            fill_installments.run(page, log, data)

        if len(data['rateio']) > 1:
            fill_cost_allocation.run(page, log, data)

        PlaywrightElement(page, '//*[@id="CONFIRMA"]', 4000).action('click')

        success_popup = PlaywrightElement(page, '#DVELOP_CONFIRMPANELContainer_ConfirmPanel > div.Body', 6000).find()

        popup_msg = success_popup.inner_text().strip()

        if 'gerada corretamente com o seguinte status: Pendente.' in popup_msg:
            PlaywrightElement(page, '#DVELOP_CONFIRMPANELContainer_ConfirmPanel > div.Footer > span > button', 3000).action('click')

            return True, f"A nota fiscal com o id {data['numero_nf']} foi inserida com sucesso!"

    except Exception as e:
        log.error(e)
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.use_cases.cadastro_nf_servico").get_logger()

    path = f'../data/cadastro_nf_produto.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'cadastro_nf_servico'):
        with BrowserAutomation() as _page:
            try:
                run(_page, _log, _data)
            except Exception as ex:
                _log.error(ex)
                pass
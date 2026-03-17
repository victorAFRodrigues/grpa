from json import load
from automations.dealernet.common import login, import_xml, select_xml, categorize_products, \
    fill_pre_product_invoice_cover, fill_product_invoice_cover, fill_installments, fill_cost_allocation, select_invoice
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime
from modules.utils.general.xml import Xml

def run(page, log, data):

    xml_path = Xml(
        data["nfexml_content"],
        data["nfexml_filename"]
    ).generate()


    try:
        login.run(page, log, data) #

        import_xml.run(page, log, xml_path)

        select_xml.run(page, log, data)

        categorize_products.run(page, log)

        fill_pre_product_invoice_cover.run(page, log, data)

        select_invoice.run(page, log, data)

        fill_product_invoice_cover.run(page, log, data)

        if len(data['parcelas']) > 1:
            fill_installments.run(page, log, data)

        if len(data['rateio']) > 1 or data['filial'] != '19':
            fill_cost_allocation.run(page, log, data)

        PlaywrightElement(page, '//*[@id="CONFIRMA"]', 4000).action('click')

        success_popup = PlaywrightElement(page, '#DVELOP_CONFIRMPANELContainer_ConfirmPanel > div.Body', 6000).find()

        popup_msg = success_popup.inner_text().strip()

        if 'Documento Fiscal Gerado Corretamente' in popup_msg:
            PlaywrightElement(page, '#DVELOP_CONFIRMPANELContainer_ConfirmPanel > div.Footer > span > button', 3000).action('click')

            return True, f"A nota fiscal com o id {data['numero_nf']} foi inserida com sucesso!"
        else:
            raise Exception("")

    except Exception as e:
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.use_cases.cadastrar_nf_produto").get_logger()

    path = f'../data/cadastrar_nf_produto.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'cadastrar_nf_produto'):
        with BrowserAutomation() as _page:
            try:
                run(_page, _log, _data)
            except Exception as ex:
                _log.error(ex)
                pass
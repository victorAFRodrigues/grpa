import json
from datetime import datetime
from automations.dealernet.common import login, import_xml, select_xml, categorize_products, \
    fill_pre_product_invoice_cover, select_invoice
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime
from modules.utils.general.xml import Xml

def run(page, log, data):

    today = datetime.now()

    year, month, day = today.year, today.month, today.day

    date = f'{day:02d}/{month:02d}/{year:04d}'

    try:
        # verify and fill row 1 the form
        PlaywrightElement(page, '#vNOTAFISCAL_NUMERO', 4000).find()
        PlaywrightElement(page, '#vNOTAFISCAL_DATAMOVIMENTO').action('write' , date)

        # fill row 2 the form
        data_chegada = PlaywrightElement(page, '#vNOTAFISCAL_DATACHEGADA')
        data_chegada.action('write' , date)
        data_chegada.action('click')


        # Fill in the remaining fields.
        select = PlaywrightElement(page, '#vNOTAFISCAL_CONDICAOPAGAMENTOCOD')
        select.find().select_option(data["condicao_pagamento"])

        select = PlaywrightElement(page, '#vAGENTECOBRADOR_CODIGO')
        select.find().select_option('10')

        if data['codigo_verificacao'] != '':
            cod_verificacao = ''

            try:
                cod_verificacao = PlaywrightElement(page, '#vNOTAFISCAL_CHAVENFE').find()
                if not cod_verificacao.is_visible():
                    raise Exception()
            except:
                cod_verificacao = PlaywrightElement(page, '#vNOTAFISCAL_CODIGOVERIFICACAO').find()
                if not cod_verificacao.is_visible():
                    raise Exception()
                else:
                    pass
            finally:
                if cod_verificacao.is_visible():
                    cod_verificacao.fill(data['codigo_verificacao'].replace(" ", ""))

        log.success("Capa da nota preenchida com sucesso!")


    except Exception as e:
        log.error(f"Não foi possivel preencher a capa da nota, erro: {e}")
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.common.fill_product_invoice_cover").get_logger()

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

            select_invoice.run(_page, _log, _data)

            run(_page, _log, _data)
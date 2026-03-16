import json
from datetime import datetime
from automations.dealernet.common import login, import_xml, select_xml, categorize_products
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime
from modules.utils.general.xml import Xml

def run(page, log, data):

    today = datetime.now()

    year, month, day = today.year, today.month, today.day

    date = f'{day:02d}/{month:02d}/{year:04d}'

    try:
        # fill row 1 the form
        select = PlaywrightElement(page, '#vNOTAFISCAL_GRUPOMOVIMENTO', 5000)
        select.find().select_option('COM')

        # fill row 2 the form
        PlaywrightElement(page, '#NATOPE').action('click')
        select = PlaywrightElement(page, '#vNOTAFISCAL_NATUREZAOPERACAOCOD')
        select.find().select_option(str(int(data["natureza_operacao"])))
        PlaywrightElement(page, '#CONFIRMAR').action('click')

        # fill row 3 the form
        select = PlaywrightElement(page, '#vPESSOA_TIPOPESSOA')
        select.find().select_option("J")

        # fill row 3 the form
        PlaywrightElement(page, '#TIPODOC').action('click')
        try:
            select = PlaywrightElement(page, '#vNOTAFISCAL_TIPODOCUMENTOCOD').find()
            select.select_option(value=data["tipo_documento"])
        except:
            pass
        PlaywrightElement(page, '#CONFIRMAR').action('click')

        # Fill in the remaining fields.
        try:
            PlaywrightElement(page,'#vNOTAFISCAL_CONTAGERENCIALCOD').action('write', data["conta_gerencial"])
        except:
            pass

        select = PlaywrightElement(page, '#vNOTAFISCAL_DEPARTAMENTOCOD')
        select.find().select_option(data["rateio"][0]['departamento'])

        select = PlaywrightElement(page, '#vNOTAFISCAL_CONDICAOPAGAMENTOCOD')
        select.find().select_option(data["condicao_pagamento"])

        select = PlaywrightElement(page, '#vAGENTECOBRADOR_CODIGO')
        select.find().select_option('10')

        PlaywrightElement(page, '#vISUTILIZAREGRATRIBUTOICMSPISCOFINS').action('click')
        # PlaywrightElement(page, '#vISUTILIZAREGRATRIBUTOSOMENTEPISCOFINS').action('click')

        try:
            select = PlaywrightElement(page, '#vNOTAFISCAL_INDICADORPRESENCA')
            select.find().select_option("0")
        except:
            pass

        PlaywrightElement(page, '#IMGPROCESSAR').action('click')

        err = PlaywrightElement(page, '#gxErrorViewer > div:nth-child(1)', 10000).find()

        if err:
            err_msg = err.inner_text().strip()

            if not err_msg == 'Nota Fiscal Processada com Sucesso':
                raise Exception(err_msg)

        log.success("Capa da nota preenchida com sucesso!")


    except Exception as e:
        log.error(f"Não foi possivel preencher a capa da nota, erro: {e}")
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.common.fill_pre_product_invoice_cover").get_logger()

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

            run(_page, _log, _data)
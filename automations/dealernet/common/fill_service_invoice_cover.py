import json
from datetime import datetime
from automations.dealernet.common import login
from core.browser_automation import BrowserAutomation, PlaywrightElement
from core.logger import Logger
from modules.utils.general.exectime import ExecTime


def run(page, log, data):

    today = datetime.now()

    year, month, day = today.year, today.month, today.day

    date = f'{day:02d}/{month:02d}/{year:04d}'

    try:
        PlaywrightElement(page, '//button[normalize-space()="Produtos"]').action('click')
        PlaywrightElement(page, '//span[normalize-space()="Nota Fiscal"]', 3000).action('move_to')
        PlaywrightElement(page, '//span[normalize-space()="NF Entrada Item Avulso"]').action('click')

        insert_btn = PlaywrightElement(page,'//*[@id="INSERT"]').find()
        insert_btn.wait_for()
        insert_btn.click()

        # fill row 1 the form
        PlaywrightElement(page, '#vNOTAFISCAL_NUMERO').action('write' , data['numero_nf'])
        PlaywrightElement(page, '#vNOTAFISCAL_SERIE').action('write' , data['serie'])
        PlaywrightElement(page, '#vNOTAFISCAL_DATAMOVIMENTO').action('write' , date)

        # fill row 2 the form
        PlaywrightElement(page, '#vNOTAFISCAL_DATAEMISSAOD').action('write' , data['data_emissao'])
        data_chegada = PlaywrightElement(page, '#vNOTAFISCAL_DATACHEGADA')
        data_chegada.action('write' , date)
        data_chegada.action('click')

        # fill row 3 the form
        select = PlaywrightElement(page, '#vNOTAFISCAL_GRUPOMOVIMENTO')
        select.find().select_option('COM')

        # fill row 4 the form
        PlaywrightElement(page, '#vNOTAFISCAL_PESSOACOD').action('write', data['codigo_fornecedor'])
        select = PlaywrightElement(page, '#vNOTAFISCAL_DEPARTAMENTOCOD')
        select.find().select_option(data['rateio'][0]["departamento"])

        # fill row 5 the form
        PlaywrightElement(page, '#NATOPE').action('click')
        select = PlaywrightElement(page, '#vNOTAFISCAL_NATUREZAOPERACAOCOD')
        select.find().select_option(str(int(data["natureza_operacao"])))
        PlaywrightElement(page, '#CONFIRMAR').action('click')
        try:
            PlaywrightElement(page,'#vNOTAFISCAL_CONTAGERENCIALCOD').action('write', data["conta_gerencial"])
        except:
            pass
        try:
            select = PlaywrightElement(page, '#vNOTAFISCAL_INDICADORPRESENCA')
            select.find().select_option("0")
        except:
            pass

        # fill row 6 the form
        PlaywrightElement(page, '#TIPODOC').action('click')
        try:
            select = PlaywrightElement(page, '#vNOTAFISCAL_TIPODOCUMENTOCOD').find()
            select.select_option(value=data["tipo_documento"])
        except:
            pass
        PlaywrightElement(page, '#CONFIRMAR').action('click')

        # Fill in the remaining fields.
        select = PlaywrightElement(page, '#vNOTAFISCAL_CONDICAOPAGAMENTOCOD')
        select.find().select_option(data["condicao_pagamento"])

        select = PlaywrightElement(page, '#vAGENTECOBRADOR_CODIGO')
        select.find().select_option('10')

        PlaywrightElement(page, '#vNOTAFISCAL_OBSERVACAO').action('write', data['observacao'])
        PlaywrightElement(page, '#vNOTAFISCAL_VALORTOTALDIGITADO').action('write', data['valor_total'])

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
                    cod_verificacao.fill(data['codigo_verificacao'])

        log.success("Capa da nota preenchida com sucesso!")


    except Exception as e:
        log.error(f"Não foi possivel preencher a capa da nota, erro: {e}")
        raise Exception(e)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.common.fill_service_invoice_cover").get_logger()

    path = f'../data/cadastrar_nf_servico.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = json.load(file)

    with ExecTime(_log, 'fill_service_invoice_cover'):
        with BrowserAutomation() as _page:
            login.run(_page, _log)

            run(_page, _log, _data)
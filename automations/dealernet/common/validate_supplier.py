from json import load
from automations.dealernet.common import login
from core.browser_automation import PlaywrightElement, BrowserAutomation
from core.logger import Logger
from modules.utils.general.exectime import ExecTime

def run (page, log, cnpj: str):
    try:
        page.get_by_role("button", name="Cadastro").click()

        page.get_by_role("link", name="Pessoas").click()

        PlaywrightElement(page, '#vPESSOA_DOCIDENTIFICADOR').action('write', cnpj)

        PlaywrightElement(page, "#IMGREFRESH").action('click')

        cod_fornecedor = PlaywrightElement(page, "#span_PESSOA_CODIGO_0001").find()

        if cod_fornecedor:
            log.success('Fornecedor encontrado!')

            return {
                'codigo': cod_fornecedor.inner_text().strip(),
                'cnpj': cnpj
            }

    except Exception as ex:
        log.error(ex)
        raise Exception(ex)

if __name__ == "__main__":
    _log = Logger('automation.dealernet.common.validate_supplier').get_logger()

    path = f'../data/validar_fornecedor.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'validate_supplier'):
        with BrowserAutomation() as _page:
            login.run(_page, _log)

            run(_page, _log, _data['cnpj'])
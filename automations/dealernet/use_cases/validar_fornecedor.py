from json import load
from automations.dealernet.common import login, validate_supplier
from core.browser_automation import BrowserAutomation
from core.logger import Logger
from modules.utils.general.exectime import ExecTime


def run(page, log, data):

    try:

        login.run(page, log, data)

        ret = validate_supplier.run(page, log, data['cnpj'])

        log.success(f"{ret}")

        return True, ret

    except Exception as ex:
        log.error("Fornecedor não encontrado!")
        raise Exception(ex)


if __name__ == '__main__':
    _log = Logger("automations.dealernet.use_cases.validar_fornecedor").get_logger()

    path = f'../data/validar_fornecedor.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'validar_fornecedor'):
        with BrowserAutomation() as _page:
            try:
                run(_page, _log, _data)
            except Exception as ex:
                _log.error(ex)
                pass
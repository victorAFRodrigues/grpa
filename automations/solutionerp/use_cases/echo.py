from json import load
from core.browser_automation import BrowserAutomation
from core.logger import Logger
from modules.utils.general.exectime import ExecTime


def run(page, log, data):

    try:

        return True, data

    except Exception as ex:
        log.error("Fornecedor não encontrado!")
        raise Exception(ex)


if __name__ == '__main__':
    _log = Logger("automations.system.use_cases.echo").get_logger()

    # Usa o json com dados mockados para teste unitario da rotina (descomentar se for utilizar)
    path = f'../data/echo.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'validar_fornecedor'):
        with BrowserAutomation() as _page:
            try:
                ret = run(_page, _log, _data)
                print(ret)
            except Exception as ex:
                _log.error(ex)
                pass
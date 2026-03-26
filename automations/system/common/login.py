from json import load
from automations.system.common import switch_filial
from core.browser_automation import PlaywrightElement, BrowserAutomation
from core.logger import Logger
from modules.utils.general.dotenv import DotEnv
from modules.utils.general.exectime import ExecTime


def run (page, log, data=None):

    env = DotEnv()

    USER = env.get("USER")
    PASSWORD = env.get("PASSWORD")
    DEALERNET_URL = env.get("SYSTEM_URL")

    try:
        page.goto(DEALERNET_URL)

        page.fill("#vUSUARIO_IDENTIFICADORALTERNATIVO", USER)
        page.fill("#vUSUARIOSENHA_SENHA", PASSWORD)
        page.click("input[id=IMAGE3]")

        PlaywrightElement(page, "#W0038TABLECENTRO", 4000).find()

        if data:
            try:
                switch_filial.run(page, log, data['filial'])
            except Exception as ex:
                log.error(ex)
                pass

        log.success("Login realizado!")

        return True

    except Exception as ex:
        log.error(ex)
        raise Exception(ex)

if __name__ == "__main__":
    _log = Logger('automations.system.common.login').get_logger()

    path = f'../data/validar_fornecedor.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'login'):
        with BrowserAutomation() as _page:
            run(_page, _log, _data)
from json import load
from core.browser_automation import PlaywrightElement, BrowserAutomation
from core.logger import Logger
from modules.utils.general.env import DotEnv
from modules.utils.general.exectime import ExecTime


def run (page, log, data=None):

    env = DotEnv()

    USER = env.get("USER")
    PASSWORD = env.get("PASSWORD")
    SYSTEM_URL = env.get("SYSTEM_URL")

    try:
        # faz as ações previstas pra efetuar o login

        print(USER)
        print(PASSWORD)
        print(SYSTEM_URL)

        log.success("Login realizado!")

        return True

    except Exception as ex:
        log.error(ex)
        raise Exception(ex)

if __name__ == "__main__":
    _log = Logger('automations.system.common.login').get_logger()

    path = f'../data/echo.json'

    with open(path, "r", encoding="utf-8") as file:
        _data = load(file)

    with ExecTime(_log, 'login'):
        with BrowserAutomation() as _page:
            run(_page, _log, _data)
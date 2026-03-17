from core.artifact_manager import ArtifactManager
from core.updater import Updater
from modules.utils.general.dotenv import DotEnv
from modules.utils.general.envupdate import EnvUpdate
from core.api import Api
from time import sleep
from json import loads
from core.worker import worker

class Main:
    def __init__(self):
        self.api = Api()

    def _main(self):
        self.api.search_update()

        with EnvUpdate():
            search_timeout = int(DotEnv().get('SEARCH_TIMEOUT'))
            response = self.api.get_task("/IniciarTarefa").json()["content"]

            if not response:
                print(f"Nenhuma Task de automação foi encontrada. Tentando novamente em {search_timeout} segundos...\n")
                sleep(search_timeout)
            else:
                response = loads(response)[0]

                _guid = response["RPA_GUID"]
                _use_case = response["RPA_SOURCE"]
                _data = loads(response["RPA_PARAMS"])
                _system = DotEnv().get('APPLICATION')

                result, msg = worker(_guid, _system, _use_case, _data)

                print(msg)

                log_b64 = ''
                screenshot_b64 = ''

                if not result:
                    am = ArtifactManager()

                    log_b64 = am.latest_log(_use_case)
                    screenshot_b64 = am.latest_screenshot()

                self.api.finish_task(
                    "/FinalizarTarefa",
                    msg,
                    "00" if result else "01",
                    _guid,
                    log_b64,
                    screenshot_b64
                )

    def test(self):
        self._main()

    def run(self):
        while True:
            self._main()


if __name__ == '__main__':
    Updater.bootstrap_automations()
    m = Main()
    m.run()
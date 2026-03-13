from json import dumps
import json
import requests
from core.updater import Updater
from modules.utils.general.dotenv import DotEnv
from modules.utils.models import GetTaskModel, ResetTaskModel, FinishTaskModel, UpdateAutomationsModel

# Classe API, ela foi criada para padronizar as requests tendo em vista que todas devem ser feitas do mesmo jeito
# seguindo de base o modelo de dados apiBodyModel
class Api:
    def __init__(self):
        self.baseUrl = DotEnv().get("API_URL")
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "goevo_app_tptoken": DotEnv().get("GOEVO_APP_TPTOKEN")
        }

    def get_task(self, endpoint):
        payload = GetTaskModel(
            RPA_EXECUTOR=DotEnv().get("RPA_EXECUTOR"),
        ).model_dump()

        response = requests.post(
            f"{self.baseUrl}{endpoint}",
            headers=self.headers,
            data=payload
        )

        response.raise_for_status()
        return response

    def reset_task(self, endpoint, guid_code):
        payload = ResetTaskModel(
            RPA_EXECUTOR=DotEnv().get("RPA_EXECUTOR"),
            RPA_GUID=guid_code
        ).model_dump()

        response = requests.post(
            f"{self.baseUrl}{endpoint}",
            headers=self.headers,
            data=payload
        )

        response.raise_for_status()
        return response

    def finish_task(self, endpoint, rpa_msg, errorcode, guid_code, logs_b64, screenshot_b64):
        finishModel = {
            "errorcode": errorcode,
            "errormsg": "",
            "content": rpa_msg
        }

        payload = FinishTaskModel(
            RPA_EXECUTOR=DotEnv().get("RPA_EXECUTOR"),
            RPA_GUID=guid_code,
            RPA_RESULT=dumps(finishModel),
            RPA_SCREENSHOT=dumps(screenshot_b64),
            RPA_LOG=dumps(logs_b64)
        ).model_dump()

        response = requests.post(
            f"{self.baseUrl}{endpoint}",
            headers=self.headers,
            data=payload
        )

        response.raise_for_status()
        return response

    def get_variables(self, endpoint):
        response = requests.post(f"{self.baseUrl}{endpoint}", headers=self.headers)
        response.raise_for_status()
        return json.loads(response.json()['content'])

    def search_update(self):
        payload = UpdateAutomationsModel(
            RPA_EXECUTOR=DotEnv().get("RPA_EXECUTOR"),
            RPA_NAME=DotEnv().get("APPLICATION").upper(),
            RPA_VERSION=DotEnv().get("GRPA_VERSION")
        ).model_dump()

        response = requests.post(
            f"{self.baseUrl}/AtualizarPacote",
            headers=self.headers,
            data=payload
        )

        response.raise_for_status()

        if response.json()['errorcode'] == "00" and response.json()['content'] != '':
            Updater.automations(response.json()['content'])

        print('Automations already updated!')

        return response

if __name__ == "__main__":
    api = Api()

    res = api.search_update()

    print(res.json())



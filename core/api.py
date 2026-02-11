from json import dumps
import json
import requests
from modules.utils.general import DotEnv
from api.database.schemas import GetTaskModel, ResetTaskModel, FinishTaskModel


# Classe API, ela foi criada para padronizar as requests tendo em vista que todas devem ser feitas do mesmo jeito
# seguindo de base o modelo de dados apiBodyModel
class Api:
    def __init__(self):
        self.baseUrl = DotEnv().get("API_URL")
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "goevo_app_tptoken": DotEnv().get("GOEVO_APP_TPTOKEN")
        }

    def getTask(self, endpoint):
        payload = GetTaskModel(
            RPA_EXECUTOR = DotEnv().get("RPA_EXECUTOR"),
        ).model_dump()

        response = requests.post(
            f"{self.baseUrl}{endpoint}", 
            headers=self.headers, 
            data=payload
        )

        response.raise_for_status()
        return response
    
    def resetTask(self, endpoint, guid_code):
        payload = ResetTaskModel(
            RPA_EXECUTOR = DotEnv().get("RPA_EXECUTOR"),
            RPA_GUID = guid_code
        ).model_dump()

        response = requests.post(
            f"{self.baseUrl}{endpoint}", 
            headers=self.headers, 
            data=payload
        )

        response.raise_for_status()
        return response
    
    def finishTask(self, endpoint, rpa_msg, errorcode, guid_code):
        finishModel = {
            "errorcode": errorcode,
            "errormsg": "",
            "content": rpa_msg
        }

        payload = FinishTaskModel(
                RPA_EXECUTOR = DotEnv().get("RPA_EXECUTOR"),
                RPA_GUID = guid_code,
                RPA_RESULT = dumps(finishModel)
            ).model_dump()

        response = requests.post(
            f"{self.baseUrl}{endpoint}", 
            headers=self.headers, 
            data=payload
        )

        response.raise_for_status()
        return response

    def getVariables(self, endpoint):
        response = requests.post(f"{self.baseUrl}{endpoint}", headers=self.headers)
        response.raise_for_status()
        return  json.loads(response.json()['content'])


if __name__ == "__main__":
    api = Api()
    
    res = api.getVariables('?Grupolelacteste/RPAManager/AtualizarVariaveis')
    # res = res.json()['content']
    # print(res if res != "" else "void")
    print(res)
    
    
        







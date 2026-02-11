from modules.core.api import Api
from modules.utils.general import DotEnv

class EnvUpdate:
    def __init__(self):
        self.api = Api()
        self.env = DotEnv()
        
    def __enter__(self):
        print(">>> Entrou no EnvUpdate")

        APP_DATA = self.api.getVariables('?Grupolelacteste/RPAManager/AtualizarVariaveis')

        for key, value in {
            "SEARCH_TIMEOUT": APP_DATA['searchTimeout'],
            "APPLICATION":  APP_DATA['application']['system'],
            "SYSTEM_URL":  APP_DATA['application']['systemUrl'],
            "USER":  APP_DATA['application']['user'],
            "PASSWORD":  APP_DATA['application']['password'],
        }.items():
            self.env.set(key, value)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

if __name__ == "__main__":
    # Rodar como modulo  
    # Command: & C:/Projetos/goevo_rpa/.venv/Scripts/python.exe -m modules.core.updater
    with EnvUpdate():
        pass

    
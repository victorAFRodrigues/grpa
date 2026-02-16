import importlib

from core.browser_automation import BrowserAutomation
from core.logger import Logger
from modules.utils.general import DotEnv

def worker(system:str, use_case:str, data: dict):
    """
    Executa dinamicamente uma automação com base no nome da tarefa e dados fornecidos.
    Retorna uma tupla: (success: bool, error_message: str | None)
    """
    log = Logger("Worker").get_logger()

    is_container = DotEnv().get('DOCKER_MODE').lower() == "true"

    if is_container:
        module_str = f"app/automations.{system}.use_cases.{use_case}"
    else:
        module_str = f"automations.{system}.use_cases.{use_case}"

    try:
        module = importlib.import_module(module_str)
        with BrowserAutomation():
            log.info(f"Iniciando automacao [{system}] - {use_case} ...")
            result, msg = module.run(data)

        if result:
            msg = msg if msg else f"Tarefa {use_case} concluída com sucesso!"
            log.success(msg)
            return True, msg
        else:
            msg = msg if msg else f"Erro ao executar {use_case}"
            log.error(msg)
            return False, msg

    except Exception as e:
        error = f"Erro ao executar {use_case}: {str(e)}"
        log.error(error)
        return False, error
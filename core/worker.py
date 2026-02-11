import importlib

from core.automation import Automation
from core.logger import Logger
from modules.utils.general import ExecTime, DotEnv

def Worker(system:str, use_case:str):
    """
    Executa dinamicamente uma automação com base no nome da tarefa e dados fornecidos.
    Retorna uma tupla: (success: bool, error_message: str | None)
    """
    log = Logger("Worker").get_logger()

    dockerRunning = DotEnv().get('DOCKER_RUNNING').lower() == "true"

    if dockerRunning:
        module_str = f"app/automations.{system}.{use_case}"
    else:
        module_str = f"automations.{system}.{use_case}"

    try:
        module = importlib.import_module(module_str)
        with Automation(use_case):
            with ExecTime(use_case):
                log.info(f"Iniciando automacao [{system}] - {use_case} ...")
                result, msg = module.run(use_case)

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
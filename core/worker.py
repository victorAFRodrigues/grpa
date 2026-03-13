import importlib
import sys

from core.browser_automation import BrowserAutomation
from core.logger import Logger
from modules.utils.general.exectime import ExecTime


def worker(guid:str, system:str, use_case:str, data: dict):
    """
    Executa dinamicamente uma automação com base no nome da tarefa e dados fornecidos.
    Retorna uma tupla: (success: bool, error_message: str | None)
    """

    module_str = f"automations.{system}.use_cases.{use_case}"

    log = Logger(module_str).get_logger()

    try:
        if module_str in sys.modules:
            del sys.modules[module_str]

        module = importlib.import_module(module_str)

        with ExecTime(log, use_case):
            with BrowserAutomation() as page:
                log.info(f"Iniciando automacao [{system}.{use_case}] | Guid: {guid}")
                result, content = module.run(page, log, data)

        log.success(f"Tarefa {use_case} concluída com sucesso!")

        return result, content

    except Exception as e:
        error = f"Erro ao executar {use_case}: {str(e)}"
        log.error(error)
        return False, error



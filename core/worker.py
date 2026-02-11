import importlib
from modules.utils.general import ExecTime, DotEnv

def Worker(RPA_SOURCE, RPA_PARAMS):
    """
    Executa dinamicamente uma automação com base no nome da tarefa e dados fornecidos.
    Retorna uma tupla: (success: bool, error_message: str | None)
    """

    try:
        module_str = f"modules.automations.{DotEnv().get('APPLICATION')}.{RPA_SOURCE}"
        module = importlib.import_module(module_str)

        with ExecTime(RPA_SOURCE):
            result, msg = module.execute(RPA_PARAMS)

        if result:
            msg = msg if msg else f"Tarefa {RPA_SOURCE} concluída com sucesso!"
            return True, msg
        else:
            msg = msg if msg else f"Erro ao executar {RPA_SOURCE}"
            return False, msg

    except Exception as e:
        error_message = f"Erro ao executar {RPA_SOURCE}: {str(e)}"
        return False, error_message
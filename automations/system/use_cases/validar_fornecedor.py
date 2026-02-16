import time
import random
from core.logger import Logger


def run(data: dict = {}):
    log = Logger("Validar Fornecedor").get_logger()

    try:
        log.info("Iniciando validação do fornecedor...")

        # Simula busca de dados
        time.sleep(1)
        log.info("Consultando base interna...")

        time.sleep(1)
        log.info("Consultando Receita Federal...")

        time.sleep(1)

        # Simula possível erro
        if random.choice([True, False]):
            raise Exception("CNPJ inválido ou situação irregular.")

        log.info("Verificando pendências financeiras...")
        time.sleep(1)

        log.success("Fornecedor validado com sucesso!")

        return True, "Fornecedor validado com sucesso"

    except Exception as e:
        error_msg = f"Erro na validação do fornecedor: {str(e)}"
        log.error(error_msg)
        return False, error_msg

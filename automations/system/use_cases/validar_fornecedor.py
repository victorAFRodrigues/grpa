from core.logger import Logger


def run():
    log = Logger('Validar Fornecedor').get_logger()

    try:
        # raise Exception('ocorreu um erro..')
        print('validar fornecedor')
        log.success('fornecedor validado com sucesso')
        return True
    except Exception as e:
        log.error(e)
        return False
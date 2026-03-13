from time import time


class ExecTime:
    def __init__(self, log, name="Bloco"):
        self.name = name
        self.log = log

    def __enter__(self):
        self.start = time()
        return self  # permite acessar atributos depois, se quiser

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time()

        self.log.info(f"O tempo de execução de '{self.name}' foi: {end - self.start:.4f} segundos\n")
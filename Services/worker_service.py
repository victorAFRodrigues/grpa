import threading
from core.worker import Worker

class WorkerService:
    def __init__(self):
        self.active_workers: dict[str, threading.Thread] = {}
        self.stop_flags: dict[str, bool] = {}

    def start_worker(self, system: str, use_case: str, is_continuous: bool = False):
        if system in self.active_workers:
            return "Worker já está rodando"

        self.stop_flags[system] = False

        def run():
            while not self.stop_flags[system]:
                worker = Worker(system, use_case)
                worker.execute()

                if not is_continuous:
                    break

        thread = threading.Thread(target=run, daemon=True)
        thread.start()

        self.active_workers[system] = thread
        return "Worker iniciado"

    def stop_worker(self, system: str):
        if system not in self.active_workers:
            return "Worker não está rodando"

        self.stop_flags[system] = True
        del self.active_workers[system]
        return "Worker parado"

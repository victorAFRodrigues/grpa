from multiprocessing import Process
from core.worker import worker

class WorkerService:
    def __init__(self):
        self.processes: dict[str, Process] = {}

    def start_worker(self, system: str, use_case: str, data: dict):
        if system in self.processes:
            return "This system is already running!"

        process = Process(
            target=worker,
            args=(system, use_case, data),
            daemon=True
        )

        process.start()
        self.processes[system] = process

        return "Worker started!"

    def stop_worker(self, system: str):
        process = self.processes.get(system)

        if not process:
            return "System {} not found or unavailable for stopping, please try again.".format(system)

        process.terminate()
        process.join()

        del self.processes[system]

        return "Worker stopped!"

import importlib


class Validate:
    @staticmethod
    def automation_exists(system, use_case):
        module_str = f"automations.{system}.use_cases.{use_case}"

        try:
            importlib.import_module(module_str)
            return True
        except ModuleNotFoundError:
            return False
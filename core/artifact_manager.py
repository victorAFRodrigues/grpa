from pathlib import Path
import base64


class ArtifactManager:

    def __init__(self):
        root = Path(__file__).resolve().parents[1]

        self.log_dir = root / "logs"
        self.screenshot_dir = root / "screenshots"

    def _to_b64(self, file_path: Path):
        with open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    def latest_log(self, module_name: str):
        files = list(self.log_dir.glob(f"*{module_name}*.log"))

        if not files:
            return None

        latest = max(files, key=lambda f: f.stat().st_mtime)

        return {
            "file": latest.name,
            "b64": self._to_b64(latest)
        }

    def latest_screenshot(self):
        files = list(self.screenshot_dir.glob("screenshot_*.png"))

        if not files:
            return None

        latest = max(files, key=lambda f: f.stat().st_mtime)

        return {
            "file": latest.name,
            "b64": self._to_b64(latest)
        }

if __name__ == "__main__":
    module = ArtifactManager()

    log = module.latest_log("validar_fornecedor")
    screenshot = module.latest_screenshot()

    print(log)
    print(screenshot)
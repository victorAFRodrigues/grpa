from pathlib import Path

from loguru import logger
import sys
import os
from datetime import datetime


class Logger:

    def __init__(self, app_name, log_dir="logs"):
        self.app_name = app_name

        # raiz do projeto
        ROOT_DIR = Path(__file__).resolve().parents[1]

        # pasta logs sempre na raiz
        self.log_dir = ROOT_DIR / log_dir
        self.log_dir.mkdir(exist_ok=True)

        log_file = self.log_dir / f"{app_name}_{datetime.now().strftime('%Y-%m-%d')}.log"

        logger.remove()

        # Console
        logger.add(
            sys.stdout,
            format="<green>{time:HH:mm:ss}</green> "
                   "[<level>{level}</level>] "
                   "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                   "{message}",
            level="DEBUG"
        )

        # Arquivo
        logger.add(
            log_file,
            rotation="10 MB",
            retention="30 days",
            encoding="utf-8",
            format="{time:YYYY-MM-DD HH:mm:ss} [{level}] {message}",
            level="DEBUG"
        )

    def get_logger(self):
        return logger


if __name__ == "__main__":
    log1 = Logger("A").get_logger()
    log2 = Logger("B").get_logger()

    log1.info("Teste")
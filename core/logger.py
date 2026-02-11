from loguru import logger
import sys
import os
from datetime import datetime


class Logger:

    def __init__(self, app_name, log_dir="../logs"):
        self.app_name = app_name
        self.log_dir = log_dir

        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(
            log_dir,
            f"{app_name}_{datetime.now().strftime('%Y-%m-%d')}.log"
        )

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
    log = Logger("RPA").get_logger()
    log.info("Hello World")
    log.warning("Hello World")
    log = Logger("RPA2").get_logger()
    log.error("Hello World")
    log.success("Hello World")
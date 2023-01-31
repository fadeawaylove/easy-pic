from loguru import logger

from src.constant import log_path


logger.add(log_path, format="{time} {level} {message}", retention="1 days", encoding="utf-8")

root_logger = logger

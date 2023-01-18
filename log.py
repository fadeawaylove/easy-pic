import os

from loguru import logger

from constant import base_path

log_path = os.path.join(base_path, "root.log")

logger.add(log_path, format="{time} {level} {message}", retention="1 days", encoding="utf-8")

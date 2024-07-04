import sys
from dataclasses import dataclass

from loguru import logger

from server.types.ctypes.error import Error


@dataclass
class Logger:
  def __post_init__(self):
    self.green()

  def green(self):
    logger.add(
      sys.stdout,
      colorize=True,
      format='<green>{time}</green> <level>{message}</level>',
    )

  def log(self, msg):
    return self.info(Error(msg))

  def debug(self, msg):
    try:
      logger.debug(msg)
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

  def info(self, msg):
    try:
      logger.info(msg)
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

  def warning(self, msg):
    try:
      logger.warning(msg)
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

  def error(self, msg: str) -> int:
    try:
      logger.error(msg)
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

  def critical(self, msg: str) -> int:
    try:
      logger.critical(msg)
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

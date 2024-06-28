from pathlib import Path
from dataclasses import dataclass

from loguru import logger

from .sys.filesystem import CacheDir
from .types.types import Date, Error
from .logger.logger import Logger


@dataclass
class LoggerToFile(Logger):
  name: str
  cache_dir: Path = None

  def __post_init__(self):
    self.cache_dir = Path(self.cache_dir) / 'logs' if self.cache_dir else CacheDir().path / 'logs'
    try:
      Path.mkdir(self.cache_dir, exist_ok=True)
    except Exception as e:
      raise (Exception(f'{Error(e)}'))
    logfile = self.cache_dir / f'{self.name}_{Date().now()}.log'
    logger.add(logfile, rotation='1 day', retention='7 days', level='DEBUG')

  def log(self, msg):
    return self.info(Error(msg))

  def debug(self, msg):
    try:
      logger.debug(f'[{Date().now()}] : {msg}')
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

  def info(self, msg):
    try:
      logger.info(f'[{Date().now()}] : {msg}')
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

  def warning(self, msg):
    try:
      logger.warning(f'[{Date().now()}] : {msg}')
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

  def error(self, msg: str) -> int:
    try:
      logger.error(f'[{Date().now()}] : {msg}')
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

  def critical(self, msg: str) -> int:
    try:
      logger.critical(f'[{Date().now()}] : {msg}')
    except Exception as e:
      raise (Exception(f'{Error(e)}'))

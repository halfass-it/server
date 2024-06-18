import logging
from pathlib import Path
import sys
from datetime import datetime


class Logger:
  def __init__(self, name: str, logs_dir: Path = None) -> None:
    level: int = logging.DEBUG
    fmt: str = '%(asctime)s - %(levelname)s - %(message)s'

    self.logger = logging.getLogger(name)
    self.logger.setLevel(level)
    formatter = logging.Formatter(fmt)

    if logs_dir:
      current_time = datetime.now().strftime('%H:%M:%S_%d-%m-%Y')
      log_file = Path(logs_dir) / f'logfile_{current_time}.log'
      file_handler = logging.FileHandler(log_file)
      file_handler.setFormatter(formatter)
      self.logger.addHandler(file_handler)
    else:
      stream_handler = logging.StreamHandler(sys.stdout)
      stream_handler.setFormatter(formatter)
      self.logger.addHandler(stream_handler)

  def __call__(self) -> logging.Logger:
    return self.logger

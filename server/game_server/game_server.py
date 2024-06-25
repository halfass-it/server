from pathlib import Path

from utils.filesystem import CacheDir
from utils.logger import Logger
from gameplay_server.game import Game


class GameServer:
  def __init__(
    self,
    ip: str,
    port: int,
    buffer_size: int,
    timeout: int,
    cache_dir: Path = None,
  ) -> None:
    self.ip: str = ip
    self.port: int = port
    self.buffer_size: int = buffer_size
    self.timeout: int = timeout
    name: str = str(__name__.split('.')[-1])
    logs_dir: Path = Path(str(CacheDir())) / 'logs' if not cache_dir else cache_dir
    self.logger: Logger = Logger(name=name, logs_dir=logs_dir)()
    self.game = Game()

from dataclasses import dataclass

from server.loggers.logger import Logger


@dataclass
class Game:
  logger: Logger

  def __post_init__(self):
    pass

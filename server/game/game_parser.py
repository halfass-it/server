from dataclasses import dataclass

from server.game.game import Game
from server.loggers.logger import Logger


@dataclass
class GameParser:
  logger: Logger

  def __post_init__(self):
    self.game = Game(self.logger)

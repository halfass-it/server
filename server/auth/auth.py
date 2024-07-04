from dataclasses import dataclass

from server.loggers.logger import Logger


@dataclass
class Auth:
  logger: Logger

  def login(self, username: str, token: str) -> bool:
    return True

  def register(self, username: str, token: str) -> bool:
    return True

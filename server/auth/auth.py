from dataclasses import dataclass

from utils.logger import Logger


@dataclass
class Auth:
  logger: Logger

  def login(self, username: str, token: str) -> bool:
    return True

  def register(self, username: str, token: str) -> bool:
    return True

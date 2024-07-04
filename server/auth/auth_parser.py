from dataclasses import dataclass

from server.loggers.logger import Logger
from server.auth.auth import Auth


@dataclass
class AuthParser:
  logger: Logger

  def __post_init__(self) -> None:
    self.auth = Auth(self.logger)

  def login(self, username: str, token: str) -> bool:
    return self.auth.login(username, token)

  def register(self, username: str, token: str) -> bool:
    return self.auth.register(username, token)

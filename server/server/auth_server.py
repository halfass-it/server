import asyncio
from pathlib import Path
from dataclasses import dataclass

from server.server.server import Server
from server.types.ctypes.network import AuthPacket
from server.auth.auth_parser import AuthParser


@dataclass
class AuthServer(Server):
  ip: str
  port: int
  buffer_size: int
  timeout: int
  cache_dir: Path = None
  server_class: str = 'auth'

  def __post_init__(
    self,
  ) -> None:
    super().__post_init__()
    self.auth_parser = AuthParser(self.logger)

  def eval(self, upstream_packet: AuthPacket):
    # TODO: Move this to AuthParser logic
    if upstream_packet.command == 'LOGIN':
      if self.auth_parser.login(upstream_packet.username, upstream_packet.token):
        return AuthPacket({
          'STATUS': 'SUCCESS',
          'USERNAME': upstream_packet.username,
        })
    if upstream_packet.command == 'REGISTER':
      if self.auth_parser.register(upstream_packet.username, upstream_packet.token):
        return AuthPacket({
          'STATUS': 'SUCCESS',
          'USERNAME': upstream_packet.username,
        })
      # --
    return AuthPacket({})

  def run(self):
    asyncio.run(super().start())

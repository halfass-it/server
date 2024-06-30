from pathlib import Path
from dataclasses import dataclass
import asyncio

from server.server import Server
from server.types.ctypes import CmdPacket, AuthPacket, GamePacket
from server.gateway import GatewayParser

@dataclass
class GatewayServer(Server):
  ip: str
  port: int
  buffer_size: int
  timeout: int
  cache_dir: Path = None
  server_class: str = 'gateway'

  def __post_init__(
    self,
  ) -> None:
    super().__post_init__()
    self.gateway_parser: GatewayParser = GatewayParser()

  def eval(self, upstream_packet: CmdPacket) -> CmdPacket:
    try:
      return CmdPacket({
        'AUTH': self.gateway_parser.forward(AuthPacket(upstream_packet.auth), self.logger),
        'GAME': self.gateway_parser.forward(GamePacket(upstream_packet.game), self.logger),
      })
    except Exception as e:
      self.logger.debug(f'[{self.server_class.upper()}_SERVER] Eval error: {e}')
      return CmdPacket({})

  def run(self):
    asyncio.run(super().start())

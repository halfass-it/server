from pathlib import Path
from dataclasses import dataclass
import asyncio

from server.server.server import Server
from server.types.ctypes import GatewayPacket, AuthPacket, GamePacket
from server.gateway.gateway_parser import GatewayParser


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
    self.gateway_parser: GatewayParser = GatewayParser(self.logger)

  def eval(self, upstream_packet: GatewayPacket) -> GatewayPacket:
    try:
      return GatewayPacket({
        'AUTH': self.gateway_parser.forward(AuthPacket(upstream_packet.auth)),
        'GAME': self.gateway_parser.forward(GamePacket(upstream_packet.game)),
      })
    except Exception as e:
      self.logger.debug(f'[{self.server_class.upper()}_SERVER] Eval error: {e}')
      return GatewayPacket({})

  def run(self):
    asyncio.run(super().start())

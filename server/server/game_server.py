from pathlib import Path
from dataclasses import dataclass
import asyncio

from server.server import Server
from server.types.ctypes import GamePacket
from server.game.game_parser import GameParser

@dataclass
class GameServer(Server):
  ip: str
  port: int
  buffer_size: int
  timeout: int
  cache_dir: Path = None
  server_class: str = 'game'

  def __post_init__(
    self,
  ) -> None:
    super().__post_init__()
    self.game_parser = GameParser()

  def eval(self, upstream_packet: GamePacket) -> GamePacket:
    return upstream_packet

  def run(self):
    asyncio.run(super().start())

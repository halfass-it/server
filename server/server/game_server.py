import asyncio
from pathlib import Path
from dataclasses import dataclass

from server.server.server import Server
from server.types.ctypes.network import GamePacket
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
    self.game_parser = GameParser(self.logger)

  def eval(self, upstream_packet: GamePacket) -> GamePacket:
    #TODO: filter in parser
    return GamePacket({
      'STATUS': 'VALID',
      'TOKEN': upstream_packet.token_data,
      'COMMAND': upstream_packet.command_data
      })

  def run(self):
    asyncio.run(super().start())

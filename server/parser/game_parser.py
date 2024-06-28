import json
from dataclasses import dataclass

from server.logger.logger import Logger
from server.types.ctypes import GamePacket
from server.game_server.game import Game


@dataclass
class Parser:
  game: Game
  logger: Logger

  def input(self, data: bytes) -> GamePacket:
    try:
      headers, json_data = data.decode('utf-8').split('\r\n\r\n', 1)
      self.logger.error(f'{json_data}')
      self.logger.debug(f'[GAME_PARSER] HTTP Headers: {", ".join(headers.splitlines())}')
      json_obj = json.loads(json_data)
      self.logger.debug(f'[GAME_PARSER] JSON Data: {json_obj}')
      return GamePacket(json_obj)
    except (json.JSONDecodeError, ValueError) as e:
      self.logger.error(f'[GAME_PARSER] Invalid JSON input: {e}')
      return GamePacket({})
    except Exception as e:
      self.logger.error(f'[GAME_PARSER] Parsing error in input: {e}')
      return GamePacket({})

  def filter(self, data: str) -> str:
    # TODO: add more filters and make it more robust
    return data.replace(' ', '').replace('\n', '').replace('\r', '')

  def output(self, game_packet: GamePacket) -> GamePacket:
    try:
      return game_packet
    except Exception as e:
      self.logger.error(f'[PARSER] Parsing error in output: {e}')
      return GamePacket({})

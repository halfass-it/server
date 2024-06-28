import json
from dataclasses import dataclass

from server.logger.logger import Logger
from server.sys.gateway import AuthGateway, GameGateway
from server.types.ctypes import AuthPacket, GamePacket, CommandPacket


@dataclass
class Parser:
  logger: Logger

  def input(self, data: bytes) -> CommandPacket:
    try:
      headers, json_data = data.decode('utf-8').split('\r\n\r\n', 1)
      self.logger.error(f'{json_data}')
      self.logger.debug(f'[COMMAND_PARSER] HTTP Headers: {", ".join(headers.splitlines())}')
      json_obj = json.loads(json_data)
      self.logger.debug(f'[COMMAND_PARSER] JSON Data: {json_obj}')
      return CommandPacket(json_obj)
    except (json.JSONDecodeError, ValueError) as e:
      self.logger.error(f'[COMMAND_PARSER] Invalid JSON input: {e}')
      return CommandPacket({})
    except Exception as e:
      self.logger.error(f'[COMMAND_PARSER] Parsing error in input: {e}')
      return CommandPacket({})

  def output(self, packet: CommandPacket) -> CommandPacket:
    try:
      auth_res_packet: AuthPacket = AuthGateway.forward(AuthPacket(packet.auth), self.logger)
      game_res_packet: GamePacket = GameGateway.forward(GamePacket(packet.game), self.logger)
      return CommandPacket({'AUTH': auth_res_packet.data, 'GAME': game_res_packet.data})
    except Exception as e:
      self.logger.error(f'[COMMAND_PARSER] Parsing error in output: {e}')
      return CommandPacket({})

import json
from dataclasses import dataclass

from server.logger.logger import Logger
from server.gateway.gateway import AuthGateway, GameGateway
from server.types.ctypes.network import Packet, CommandPacket, AuthPacket, GamePacket


@dataclass
class GateParser:
  logger: Logger

  def input(
    self, data: bytes, T: Packet | CommandPacket | AuthPacket | GamePacket
  ) -> Packet | CommandPacket | AuthPacket | GamePacket:
    try:
      headers, json_data = data.decode('utf-8').split('\r\n\r\n', 1)
      self.logger.error(f'{json_data}')
      self.logger.debug(f'[GATEPARSER] HTTP Headers: {", ".join(headers.splitlines())}')
      json_obj = json.loads(json_data)
      self.logger.debug(f'[GATEPARSER] JSON Data: {json_obj}')
      return T(json_data)
    except (json.JSONDecodeError, ValueError) as e:
      self.logger.error(f'[GATEPARSER] Invalid JSON input: {e}')
      return T({})
    except Exception as e:
      self.logger.error(f'[GATEPARSER] Parsing error in input: {e}')
      return T({})

  def output(self, packet: Packet | CommandPacket | AuthPacket | GamePacket) -> bytes:
    try:
      if isinstance(packet, CommandPacket):
        auth_res_packet: AuthPacket = AuthGateway.forward(AuthPacket(packet.auth), self.logger)
        game_res_packet: GamePacket = GameGateway.forward(GamePacket(packet.game), self.logger)
        return CommandPacket({'AUTH': auth_res_packet.data, 'GAME': game_res_packet.data})
      if isinstance(packet, AuthPacket):
        return AuthGateway.forward(packet.data, self.logger)
      if isinstance(packet, GamePacket):
        return AuthGateway.forward(packet.data, self.logger)
      return Packet({})
    except Exception as e:
      self.logger.error(f'[GATEPARSER] Parsing error in output: {e}')
      return Packet({})

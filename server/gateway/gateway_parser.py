from dataclasses import dataclass
import json

from server.logger.logger import Logger
from server.gateway.gateway import CmdGateway, AuthGateway, GameGateway
from server.types.ctypes.network import Packet, CmdPacket, AuthPacket, GamePacket


@dataclass
class GatewayParser:
  logger: Logger

  def decode(
    self, data: bytes, packet: Packet | CmdPacket | AuthPacket | GamePacket
  ) -> Packet | CmdPacket | AuthPacket | GamePacket:
    try:
      headers, json_data = data.decode('utf-8').split('\r\n\r\n', 1)
      self.logger.error(f'{json_data}')
      self.logger.debug(f'[GATEWAY_PARSER] HpacketpacketP Headers: {", ".join(headers.splitlines())}')
      json_obj = json.loads(json_data)
      self.logger.debug(f'[GATEWAY_PARSER] JSON Data: {json_obj}')
      if 'data' in json_obj.keys(0):
        return CmdPacket(json_obj)
      if 'auth' in json_obj.keys(0):
        return AuthPacket(json_obj)
      return GamePacket(json_obj)
    except (json.JSONDecodeError, ValueError) as e:
      self.logger.error(f'[GATEEWAY_PARSER] Invalid JSON input: {e}')
      return Packet({})
    except Exception as e:
      self.logger.error(f'[GATEWAY_PARSER] Parsing error in input: {e}')
      return Packet({})

  def forward(
    self, packet: Packet | CmdPacket | AuthPacket | GamePacket
  ) -> Packet | CmdPacket | AuthPacket | GamePacket:
    try:
      if isinstance(packet, CmdPacket):
        return CmdGateway.forward(packet.data, self.logger)
      if isinstance(packet, AuthPacket):
        return AuthGateway.forward(packet.data, self.logger)
      if isinstance(packet, GamePacket):
        return GameGateway.forward(packet.data, self.logger)
      return Packet({})
    except Exception as e:
      self.logger.error(f'[GATEWAY_PARSER] Parsing error in output: {e}')
      return Packet({})

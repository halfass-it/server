from dataclasses import dataclass

from server.loggers.logger import Logger
from server.gateway.gateway import Gateway
from server.types.ctypes.network import Packet, GatewayPacket, AuthPacket, GamePacket


@dataclass
class GatewayParser:
  logger: Logger

  def forward(
    self, packet: Packet | GatewayPacket | AuthPacket | GamePacket, url: str = '', method: str = 'POST'
  ) -> Packet | GatewayPacket | AuthPacket | GamePacket:
    try:
      if url:
        return Gateway.forward(url, self.method, packet.data, self.logger)
      if isinstance(packet, GatewayPacket):
        return Gateway.forward(Gateway.HTTP_CMD_SERVER, self.method, packet.data, self.logger)
      if isinstance(packet, AuthPacket):
        return Gateway.forward(Gateway.HTTP_AUTH_SERVER, self.method, packet.data, self.logger)
      if isinstance(packet, GamePacket):
        return Gateway.forward(Gateway.HTTP_GAME_SERVER, self.method, packet.data, self.logger)
      return Packet({})
    except Exception as e:
      self.logger.error(f'[GATEWAY_PARSER] Parsing error in output: {e}')
      return Packet({})

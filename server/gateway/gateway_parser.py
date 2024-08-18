from dataclasses import dataclass

from server.loggers.logger import Logger
from server.gateway.gateway import Gateway
from server.types.ctypes.network import (
  Packet,
  GatewayPacket,
  AuthPacket,
  GamePacket,
)


@dataclass
class GatewayParser:
  logger: Logger

  def __post_init__(self) -> None:
    self.gateway = Gateway(logger=self.logger)

  def forward(
    self, packet: Packet | GatewayPacket | AuthPacket | GamePacket
  ) -> Packet | GatewayPacket | AuthPacket | GamePacket:
    method: str = 'POST'
    try:
      if isinstance(packet, GatewayPacket):
        return self.gateway.forward(
          url=self.gateway.HTTP_GATEWAY_SERVER,
          method=method,
          packet=packet,
        )
      if isinstance(packet, AuthPacket):
        print("I AN AUTH PACKET")
        return self.gateway.forward(
          url=self.gateway.HTTP_AUTH_SERVER,
          method=method,
          packet=packet,
        )
      if isinstance(packet, GamePacket):
        return self.gateway.forward(
          url=self.gateway.HTTP_GAME_SERVER,
          method=method,
          packet=packet,
        )
      return self.gateway.faux_forward(packet)
    except Exception as e:
      self.logger.error(f'[GATEWAY_PARSER] Parsing error in output: {e}')
      return self.gateway.faux_forward(packet)

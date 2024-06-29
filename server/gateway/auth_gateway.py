from dataclasses import dataclass

from server.types.ctypes.network import Packet, AuthPacket
from server.loggers.logger import Logger

from .gateway import Gateway


@dataclass
class AuthGateway(Gateway):
  @staticmethod
  def forward(packet: Packet | AuthPacket, logger: Logger) -> Packet | AuthPacket:
    ret_packet: Packet | AuthPacket = super().forward(super().HTTP_AUTH_SERVER, 'POST', packet, logger)
    try:
      if isinstance(ret_packet, AuthPacket):
        return AuthPacket(ret_packet.data)
      if isinstance(ret_packet, Packet):
        return Packet({})
    except Exception as e:
      logger.debug(f'[AUTH_GATEWAY] - {e}')
      return Packet({})

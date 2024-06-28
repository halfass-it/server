from dataclasses import dataclass

from server.types.ctypes.network import Packet, AuthPacket, GamePacket
from server.logger.logger import Logger

from .gateway import Gateway


@dataclass
class CommandGateway(Gateway):
  @staticmethod
  def forward(packet: Packet | AuthPacket | GamePacket, logger: Logger) -> Packet | AuthPacket | GamePacket:
    try:
      ret_packet: Packet | AuthPacket | GamePacket = super().forward(
        super().HTTP_COMMAND_SERVER, 'POST', packet, logger
      )
      if isinstance(ret_packet, Packet):
        return Packet({})
      if isinstance(ret_packet, AuthPacket):
        return AuthPacket(ret_packet.data)
      if isinstance(ret_packet, GamePacket):
        return GamePacket(ret_packet.data)
    except Exception as e:
      logger.debug(f'[COMMAND_GATEWAY] - {e}')
      return Packet({})

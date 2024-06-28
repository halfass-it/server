from dataclasses import dataclass

from server.types.ctypes.network import Packet, AuthPacket, GamePacket
from server.logger.logger import Logger

from .gateway import Gateway


@dataclass
class CommandGateway(Gateway):
  @staticmethod
  def forward(packet: Packet | AuthPacket | GamePacket, logger: Logger) -> AuthPacket | GamePacket:
    try:
      ret_packet: Packet | AuthPacket | GamePacket = Gateway.forward(
        Gateway.HTTP_COMMAND_SERVER, 'POST', packet, logger
      )
      if isinstance(ret_packet, Packet):
        return Packet(ret_packet.data)
      if isinstance(ret_packet, AuthPacket):
        return AuthPacket(ret_packet.data)
      if isinstance(ret_packet, GamePacket):
        return GamePacket(ret_packet.data)
    except Exception as e:
      logger.debug(f'[COMMAND_GATEWAY] CommandGateway exception: {e}')
      return Gateway.faux_forward(AuthPacket({})) if 'AUTH' in packet.data else Gateway.faux_forward(GamePacket({}))

from dataclasses import dataclass

from server.types.ctypes.network import Packet, GamePacket
from server.logger.logger import Logger

from .gateway import Gateway


@dataclass
class GameGateway(Gateway):
  @staticmethod
  def forward(packet: Packet | GamePacket, logger: Logger) -> Packet | GamePacket:
    try:
      ret_packet: Packet | GamePacket = super().forward(super().HTTP_GAME_SERVER, 'POST', packet, logger)
      if isinstance(ret_packet, GamePacket):
        return GamePacket(ret_packet.data)
      if isinstance(ret_packet, Packet):
        return Packet({})
    except Exception as e:
      logger.debug(f'[GAME_GATEWAY]: {e}')
      return Packet({})

from dataclasses import dataclass

from server.types.ctypes.network import Packet, CmdPacket
from server.loggers.logger import Logger

from .gateway import Gateway


@dataclass
class CmdGateway(Gateway):
  @staticmethod
  def forward(packet: Packet | CmdPacket, logger: Logger) -> Packet | CmdPacket:
    try:
      ret_packet: Packet | CmdPacket = super().forward(super().HTTP_COMMAND_SERVER, 'POST', packet, logger)
      if isinstance(ret_packet, Packet):
        return Packet({})
      if isinstance(ret_packet, CmdPacket):
        return CmdPacket(ret_packet.data)
    except Exception as e:
      logger.debug(f'[COMMAND_GATEWAY] - {e}')
      return Packet({})

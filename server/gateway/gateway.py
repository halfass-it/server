from dataclasses import dataclass

import requests

from server.loggers.logger import Logger
from server.types.ctypes.network import Packet, GatewayPacket, AuthPacket, GamePacket


@dataclass
class Gateway:
  CMD_SERVER: str = 'localhost:5000'
  AUTH_SERVER: str = 'localhost:6000'
  GAME_SERVER: str = 'localhost:7000'
  HTTP_CMD_SERVER: str = f'http://{CMD_SERVER}'
  HTTP_AUTH_SERVER: str = f'http://{AUTH_SERVER}'
  HTTP_GAME_SERVER: str = f'http://{GAME_SERVER}'

  @staticmethod
  def faux_forward(
    packet: Packet | GatewayPacket | AuthPacket | GamePacket,
  ) -> Packet | GatewayPacket | AuthPacket | GamePacket:
    return packet

  @staticmethod
  def forward(
    url: str, method: str, packet: Packet | GatewayPacket | AuthPacket | GamePacket, logger: Logger
  ) -> Packet | GatewayPacket | AuthPacket | GamePacket:
    if isinstance(packet, Packet):
      return Gateway.faux_forward(Packet({}))
    try:
      if method == 'GET':
        res = requests.get(url, json=packet.data)
      elif method == 'POST':
        res = requests.post(url, json=packet.data)
      else:
        logger.debug(f'[GATEWAY] - Unsupported HTTP method: {method}')
        return Gateway.faux_forward(Packet({}))
      if isinstance(packet, GatewayPacket):
        return GatewayPacket(res.json())
      if isinstance(packet, AuthPacket):
        return AuthPacket(res.json())
      if isinstance(packet, GamePacket):
        return GamePacket(res.json())
      return Gateway.faux_forward(Packet({}))
    except requests.exceptions.RequestException as e:
      logger.debug(f'[GATEWAY] - {e}')
      return Gateway.faux_forward(Packet({}))
    except Exception as e:
      logger.debug(f'[GATEWAY] - {e}')
      return Gateway.faux_forward(Packet({}))

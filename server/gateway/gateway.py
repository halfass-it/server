from dataclasses import dataclass

import requests

from server.loggers.logger import Logger
from server.types.ctypes.network import Packet, GatewayPacket, AuthPacket, GamePacket


@dataclass
class Gateway:
  logger: Logger
  GATEWAY_SERVER: str = 'localhost:5000'
  AUTH_SERVER: str = 'localhost:6000'
  GAME_SERVER: str = 'localhost:7000'
  HTTP_GATEWAY_SERVER: str = f'http://{GATEWAY_SERVER}'
  HTTP_AUTH_SERVER: str = f'http://{AUTH_SERVER}'
  HTTP_GAME_SERVER: str = f'http://{GAME_SERVER}'

  def faux_forward(
    self, packet: Packet | GatewayPacket | AuthPacket | GamePacket
  ) -> Packet | GatewayPacket | AuthPacket | GamePacket:
    return packet

  def forward(
    self, url: str, method: str, packet: Packet | GatewayPacket | AuthPacket | GamePacket
  ) -> Packet | GatewayPacket | AuthPacket | GamePacket:
    try:
      if method == 'GET':
        res = requests.get(url, json=packet.data)
      elif method == 'POST':
        res = requests.post(url, json=packet.data)
      else:
        self.logger.debug(f'[GATEWAY] - Unsupported HTTP method: {method}')
        return self.faux_forward(Packet({}))
      if isinstance(packet, GatewayPacket):
        return GatewayPacket(res.json())
      if isinstance(packet, AuthPacket):
        return AuthPacket(res.json())
      if isinstance(packet, GamePacket):
        return GamePacket(res.json())
      return self.faux_forward(packet)
    except requests.exceptions.RequestException as e:
      self.logger.debug(f'[GATEWAY] - {e}')
      return self.faux_forward(packet)
    except Exception as e:
      self.logger.debug(f'[GATEWAY] - {e}')
      return self.faux_forward(packet)

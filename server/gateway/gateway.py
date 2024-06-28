from dataclasses import dataclass

import requests

from server.types.ctypes.network import Packet
from server.logger.logger import Logger


@dataclass
class Gateway:
  COMMAND_SERVER: str = 'localhost:5000'
  AUTH_SERVER: str = 'localhost:6000'
  GAME_SERVER: str = 'localhost:7000'
  HTTP_COMMAND_SERVER: str = f'http://{COMMAND_SERVER}'
  HTTP_AUTH_SERVER: str = f'http://{AUTH_SERVER}'
  HTTP_GAME_SERVER: str = f'http://{GAME_SERVER}'

  @staticmethod
  def faux_forward(packet: Packet) -> Packet:
    return packet

  @staticmethod
  def forward(url: str, method: str, packet: Packet, logger: Logger) -> Packet:
    try:
      if method == 'GET':
        res = requests.get(url, json=packet.data)
      elif method == 'POST':
        res = requests.post(url, json=packet.data)
      else:
        logger.debug(f'[GATEWAY] Unsupported HTTP method: {method}')
        return Gateway.faux_forward(Packet({}))
      return Gateway.forward(Packet(res.json()))
    except requests.exceptions.RequestException as e:
      logger.debug(f'[GATEWAY] Gateway request exception: {e}')
      return Gateway.faux_forward(Packet({}))
    except Exception as e:
      logger.debug(f'[GATEWAY]  Gateway exception: {e}')
      return Gateway.faux_forward(Packet({}))

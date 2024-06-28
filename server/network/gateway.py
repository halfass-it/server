from dataclasses import dataclass

import requests
from requests.exceptions import RequestException

from utils.packet import Packet, AuthPacket, GamePacket
from utils.logger import Logger


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
    except RequestException as e:
      logger.debug(f'[GATEWAY] Gateway request exception: {e}')
      return Gateway.faux_forward(Packet({}))
    except Exception as e:
      logger.debug(f'[GATEWAY]  Gateway exception: {e}')
      return Gateway.faux_forward(Packet({}))


@dataclass
class AuthGateway(Gateway):
  @staticmethod
  def forward(auth_packet: AuthPacket, logger: Logger) -> AuthPacket:
    try:
      packet: Packet = Packet(auth_packet.data)
      res_packet: Packet = Gateway.forward(Gateway.HTTP_AUTH_SERVER, 'POST', packet, logger)
      return AuthPacket(res_packet.data)
    except Exception as e:
      logger.debug(f'[GATEWAY] AuthGateway exception: {e}')
      return AuthPacket({})


@dataclass
class GameGateway(Gateway):
  @staticmethod
  def forward(game_packet: GamePacket, logger: Logger) -> GamePacket:
    try:
      packet = Packet(game_packet.data)
      res_packet: Packet = Gateway.proxy_http(Gateway.HTTP_GAME_SERVER, 'POST', packet, logger)
      return GamePacket(res_packet.data)
    except Exception as e:
      logger.debug(f'[GATEWAY] GameGateway exception: {e}')
      return GamePacket({})


class CommandGateway(Gateway):
  @staticmethod
  def forward(packet: AuthPacket | GamePacket, logger: Logger) -> AuthPacket | GamePacket:
    try:
      packet = Packet(packet.data)
      res_packet: Packet = Gateway.forward(Gateway.HTTP_COMMAND_SERVER, 'POST', packet, logger)
      return AuthPacket(res_packet.data) if 'AUTH' in res_packet.data else GamePacket(res_packet.data)
    except Exception as e:
      logger.debug(f'[GATEWAY] CommandGateway exception: {e}')
      return Gateway.faux_forward(AuthPacket({})) if 'AUTH' in packet.data else Gateway.faux_forward(GamePacket({}))

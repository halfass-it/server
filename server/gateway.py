from dataclasses import dataclass

import requests
from requests.exceptions import RequestException

from utils.packet import Packet, AuthPacket, CommandPacket, GamePacket
from utils.logger import Logger


@dataclass
class Gateway:
  AUTH_SERVER: str = 'localhost:6000'
  GAME_SERVER: str = 'localhost:7000'
  HTTP_AUTH_SERVER: str = f'http://{AUTH_SERVER}'
  HTTP_GAME_SERVER: str = f'http://{GAME_SERVER}'

  @staticmethod
  def proxy(packet: Packet) -> Packet:
    return packet

  @staticmethod
  def proxy_http(url: str, method: str, packet: Packet, logger: Logger) -> Packet:
    try:
      if method == 'GET':
        res = requests.get(url, json=packet.data)
      elif method == 'POST':
        res = requests.post(url, json=packet.data)
      else:
        logger.debug(f'[GATEWAY] Unsupported HTTP method: {method}')
        return Gateway.proxy(Packet({}))
      return Gateway.proxy(Packet(res.json()))
    except RequestException as e:
      logger.debug(f'[GATEWAY] Gateway request exception: {e}')
      return Gateway.proxy(Packet({}))
    except Exception as e:
      logger.debug(f'[GATEWAY]  Gateway exception: {e}')
      return Gateway.proxy(Packet({}))


@dataclass
class AuthGateway(Gateway):
  @staticmethod
  def proxy(auth_packet: AuthPacket, logger: Logger) -> AuthPacket:
    try:
      packet: Packet = Packet(auth_packet.data)
      res_packet: Packet = Gateway.proxy_http(Gateway.HTTP_AUTH_SERVER, 'POST', packet, logger)
      return AuthPacket(res_packet.data)
    except Exception as e:
      logger.debug(f'[GATEWAY] AuthGateway exception: {e}')
      return AuthPacket({})


@dataclass
class GameGateway(Gateway):
  @staticmethod
  def proxy(game_packet: GamePacket, logger: Logger) -> GamePacket:
    try:
      packet = Packet(game_packet.data)
      res_packet: Packet = Gateway.proxy_http(Gateway.HTTP_GAME_SERVER, 'POST', packet, logger)
      return GamePacket(res_packet.data)
    except Exception as e:
      logger.debug(f'[GATEWAY] GameGateway exception: {e}')
      return GamePacket({})


@dataclass
class ServerGateway(Gateway):
  @staticmethod
  def forward(command_packet: CommandPacket, logger: Logger) -> CommandPacket:
    try:
      auth_res_packet: AuthPacket = AuthGateway.proxy(AuthPacket(command_packet.auth), logger)
      game_res_packet: GamePacket = GameGateway.proxy(GamePacket(command_packet.game), logger)
      return CommandPacket({'AUTH': auth_res_packet.data, 'GAME': game_res_packet.data})
    except AttributeError as e:
      logger.debug(f'[GATEWAY] AttributeError in ServerGateway: {e}')
      return CommandPacket({})
    except Exception as e:
      logger.debug(f'[GATEWAY] Unexpected error in ServerGateway: {e}')
      return CommandPacket({})

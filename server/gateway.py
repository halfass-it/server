from dataclasses import dataclass
import requests

from utils.packet import Packet, AuthPacket, CommandPacket, GamePacket
from utils.logger import Logger


@dataclass
class Gateway:
  @staticmethod
  def evaluate(packet: Packet):
    return packet


@dataclass
class AuthGateway(Gateway):
  @staticmethod
  def evaluate(auth_packet: AuthPacket, logger: Logger) -> AuthPacket:
    try:
      res = requests.post('http://localhost:6000/', json=auth_packet.data)
    except requests.RequestException as e:
      logger.error(f'[ERROR] AuthGateway requests exception: {e}')
      return auth_packet
    except Exception as e:
      logger.error(f'[ERROR] AuthGateway exception: {e}')
      return auth_packet
    return res.json()


@dataclass
class GameGateway(Gateway):
  @staticmethod
  def evaluate(game_packet: GamePacket, logger: Logger) -> GamePacket:
    try:
      res = requests.post('http://localhost:7000/', json=game_packet.data)
    except requests.RequestException as e:
      logger.error(f'[ERROR] GameGateway requests exception: {e}')
      return game_packet
    except Exception as e:
      logger.error(f'[ERROR] GameGateway exception: {e}')
      return game_packet
    return res.json()


@dataclass
class ServerGateway(Gateway):
  def evaluate(command_packet: CommandPacket) -> CommandPacket:
    game_packet: GamePacket = GamePacket(command_packet.game)
    auth_packet: AuthPacket = AuthPacket(command_packet.auth)
    return CommandPacket({
      'auth': AuthGateway.evaluate(auth_packet),
      'game': GameGateway.evaluate(game_packet),
    })

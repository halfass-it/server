from dataclasses import dataclass
import requests

from utils.packet import (
  Packet, 
  AuthPacket, 
  CommandPacket, 
  GamePacket
)

@dataclass
class Gateway:
  @staticmethod
  def evaluate(packet: Packet):
    return packet


@dataclass
class AuthGateway(Gateway):
  @staticmethod
  def evaluate(auth_packet: AuthPacket) -> AuthPacket:
    try:
      response = requests.post(
        'http://localhost:6000/',
        json=auth_packet.data
      )
      response.raise_for_status()
    except requests.RequestException as e:
      # raise requests.RequestException(f'Error: {e}')
      pass
    return auth_packet
  
@dataclass
class GameGateway(Gateway):
  @staticmethod
  def evaluate(game_packet: GamePacket) -> GamePacket:
    try:
      response = requests.post(
        'http://localhost:7000/',
        json=game_packet.data
      )
      response.raise_for_status()
    except requests.RequestException as e:
      # raise requests.RequestException(f'Error: {e}')
      pass
    return game_packet


@dataclass
class ServerGateway(Gateway):
  def evaluate(command_packet: CommandPacket) -> CommandPacket:
    game_packet: GamePacket = GamePacket(command_packet.game)
    auth_packet: AuthPacket = AuthPacket(command_packet.auth)
    return CommandPacket({'auth': AuthGateway.evaluate(auth_packet), 'game': GameGateway.evaluate(game_packet)})

from dataclasses import dataclass

from server.packet import Packet, AuthPacket, CommandPacket, GamePacket


@dataclass
class Gateway:
  @staticmethod
  def evaluate(packet: Packet):
    return packet


@dataclass
class AuthGateway(Gateway):
  @staticmethod
  def evaluate(auth_packet: AuthPacket) -> AuthPacket:
    return auth_packet


@dataclass
class GameGateway(Gateway):
  @staticmethod
  def evaluate(game_packet: GamePacket) -> GamePacket:
    return game_packet


@dataclass
class ServerGateway(Gateway):
  def evaluate(command_packet: CommandPacket) -> CommandPacket:
    game_packet: GamePacket = GamePacket(command_packet.game_data)
    auth_packet: AuthPacket = AuthPacket(command_packet.auth_data)
    return CommandPacket({'auth': AuthGateway.evaluate(auth_packet), 'game': GameGateway.evaluate(game_packet)})

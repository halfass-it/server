from dataclasses import dataclass

from server.packet import Packet, AuthPacket, CommandPacket, GameplayPacket

@dataclass(frozen=True)
class Gateway:
  @staticmethod
  def evaluate(packet: Packet):
    return packet
  
@dataclass(frozen=True)
class AuthGateway(Gateway):
  @staticmethod
  def evaluate(auth_packet: AuthPacket) -> AuthPacket:
    return auth_packet  

@dataclass(frozen=True)
class GameplayGateway(Gateway):
  @staticmethod
  def evaluate(gameplay_packet: GameplayPacket) -> GameplayPacket:
    return gameplay_packet
  
@dataclass(frozen=True)
class ServerGateway(Gateway):
  def evaluate(command_packet: CommandPacket) -> CommandPacket:
    gameplay_packet: GameplayPacket = GameplayPacket(command_packet['gameplay'])
    auth_packet: AuthPacket = AuthPacket(command_packet['auth'])
    return CommandPacket({
      'auth': AuthGateway.evaluate(auth_packet),
      'gameplay': AuthGateway.evaluate(gameplay_packet)
    })




  
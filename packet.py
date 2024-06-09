import json
import enum
from dataclasses import dataclass

# ================== Command ==================

@dataclass
class Command(enum.Enum): 
  def __post__init__(self) -> None:
    self.packet_name = None
    self.packet_class = None

@dataclass
class ChatCommand(Command):
  def __post__init__(self) -> None:
    self.packet_name = 'chat'
    self.packet_class = 'ChatPacket'

# ================== - ==================
    
# ================== Packet ==================
    
@dataclass
class Packet:
  def __post_init__(self, command: Command, *payloads: tuple) -> None:
    self.command = command
    self.payloads: tuple = payloads

  def __str__(self) -> str:
    serialise_dict = {'a': self.command.name}
    for i in range(len(self.payloads)):
      serialise_dict[f'p{i}'] = self.payloads[i]
    data = json.dumps(serialise_dict, separators=(',', ':'))
    return data

  def __bytes__(self) -> bytes:
    return str(self).encode('utf-8')

@dataclass
class ChatPacket(Packet):
  def __post__init__(self, command: ChatCommand, *payloads: tuple) -> None:
    super().__post_init__(command, payloads)

# ================== - ==================

# ================== PacketParser ==================
    
@dataclass
class PacketParser:
  @staticmethod
  def from_json(data: bytes) -> Packet:
    deserialise_dict = json.loads(data)
    command: Command = None
    payloads: list = []
    for key, value in deserialise_dict.items():
      if key == 'chat':
        command = ChatCommand()
      elif key[0] == 'p':
        i = int(key[1:])
        payloads.insert(i, value)
    return PacketParser.build_packet(command, payloads)
  
  @staticmethod
  def build_packet(command: Command, payloads: list):
    try:
      constructor: type = globals()[command.packet_class]
      return constructor(command, *payloads)
    except KeyError as e:
      print(f"{command.packet_class} is not a valid packet class. Stacktrace: {e}")
    except TypeError as e:
      print(f"{command.packet_class} doesn't support the given payloads {tuple(payloads)}. Stacktrace: {e}")

# ================== - ==================

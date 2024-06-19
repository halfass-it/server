from dataclasses import dataclass, field

from server.types import AuthPacketStructure, GameplayPacketStructure, CommandPacketStruct

@dataclass
class Packet:
  category: str = field(init=False)

  def __str__(self) -> str:
    return ''

  def __repr__(self) -> str:
    return f'{self.category}()'
  
@dataclass
class AuthPacket(Packet):
  category: str = field(init=False, default='AuthPacket')
  data: AuthPacketStructure

  def __post_init__(self):
        super().__post_init__()

  def __str__(self) -> str:
    return self.data

  def __bytes__(self) -> bytes:
        return str(self.data).encode('utf-8')

  def __repr__(self) -> str:
      return f'{self.category}({self.data})'

@dataclass
class GameplayPacket(Packet):
  category: str = field(init=False, default='GameplayPacket')
  data: GameplayPacketStructure

  def __post_init__(self):
        super().__post_init__()

  def __str__(self) -> str:
    return self.data

  def __bytes__(self) -> bytes:
        return str(self.data).encode('utf-8')

  def __repr__(self) -> str:
      return f'{self.category}({self.data})'
  
@dataclass
class CommandPacket(Packet):
  category: str = field(init=False, default='CommandPacket')
  data: CommandPacketStruct

  def __post_init__(self):
        super().__post_init__()

  def __str__(self) -> str:
    return self.data

  def __bytes__(self) -> bytes:
        return str(self.data).encode('utf-8')

  def __repr__(self) -> str:
      return f'{self.category}({self.data})'
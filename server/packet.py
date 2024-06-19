from dataclasses import dataclass, field

from server.types import AuthPacketStructure, GamePacketStructure, CommandPacketStruct


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

    def __str__(self) -> str:
        return self.data

    def __bytes__(self) -> bytes:
        return str(self.data).encode('utf-8')

    def __repr__(self) -> str:
        return f'{self.category}({self.data})'


@dataclass
class GamePacket(Packet):
    category: str = field(init=False, default='GamePacket')
    data: GamePacketStructure

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
      self.auth_data = self.data.get('auth', {})
      self.game_data = self.data.get('game', {})

    def __str__(self) -> str:
        return f"auth: {self.auth_data}, game: {self.game_data}"

    def __bytes__(self) -> bytes:
        return str(self.data).encode('utf-8')

    def __repr__(self) -> str:

        return f'{self.category}(auth={self.auth_repr}, game={self.game_repr})'

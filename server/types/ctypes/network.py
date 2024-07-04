from dataclasses import dataclass, field

from server.types.dtypes.network import packet, gateway_packet, auth_packet, game_packet


@dataclass
class Packet:
  category: str = field(init=False, default='Packet')
  data: packet

  def __str__(self) -> str:
    return str(self.data)

  def __bytes__(self) -> bytes:
    return str(self.data).encode('utf-8')

  def __repr__(self) -> str:
    return f'{self.category}()'


@dataclass
class AuthPacket(Packet):
  category: str = field(init=False, default='AuthPacket')
  data: auth_packet

  def __post_init__(self):
    self.update()

  def update(self):
    self.username = self.data.get('username', '')
    self.token = self.data.get('token', '')
    self.command = self.data.get('command', '')
    self.status = self.data.get('status', '')

  def __str__(self) -> str:
    return str(self.data)

  def __bytes__(self) -> bytes:
    return str(self.data).encode('utf-8')

  def __repr__(self) -> str:
    return f'{self.category}({self.data})'


@dataclass
class GamePacket(Packet):
  category: str = field(init=False, default='GamePacket')
  data: game_packet

  def __post_init__(self):
    self.update()

  def update(self):
    return

  def __str__(self) -> str:
    return str(self.data)

  def __bytes__(self) -> bytes:
    return str(self.data).encode('utf-8')

  def __repr__(self) -> str:
    return f'{self.category}({self.data})'


@dataclass
class GatewayPacket(Packet):
  category: str = field(init=False, default='GatewayPacket')
  data: gateway_packet

  def __post_init__(self):
    self.update()

  def update(self):
    self.auth_data = self.data.get('AUTH', {})
    self.game_data = self.data.get('GAME', {})

  def __str__(self) -> str:
    return str({'AUTH': self.auth_data, 'GAME': self.game_data})

  def __bytes__(self) -> bytes:
    return str({'AUTH': self.auth_data, 'GAME': self.game_data}).encode('utf-8')

  def __repr__(self) -> str:
    return f'{self.category}(AUTH={repr(self.auth_data)}, GAME={repr(self.game_data)})'

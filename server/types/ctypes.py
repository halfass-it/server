import datetime
import inspect
import traceback
from dataclasses import dataclass, field

from .dtypes import packet, command_packet, auth_packet, game_packet


@dataclass
class Error:
  msg: str
  error_type: str = None
  stacktrace: str = None
  error_msg: str = field(init=False)

  def __post_init__(self):
    caller_frame = inspect.currentframe().f_back
    file_path = inspect.getfile(caller_frame)
    method_name = caller_frame.f_code.co_name
    line_number = caller_frame.f_lineno
    if self.error_type is None:
      self.error_type = 'GenericError'
    if self.stacktrace is None:
      self.stacktrace = ''.join(traceback.format_stack()[:-1])
    self.error_msg = (
      f'[ERROR] {self.error_type}: {self.msg}\n'
      f'Location: {file_path}:{method_name}:{line_number}\n'
      f'Stacktrace:\n{self.stacktrace}'
    )

  def __str__(self):
    return self.error_msg

  def __repr__(self):
    return f"Error(msg='{self.msg}', error_type='{self.error_type}')"


@dataclass
class Date:
  date: str = None

  def now(self):
    self.date = Date(datetime.datetime.now().strftime('%H-%M-%S_%d-%m-%Y'))
    return self.date

  def __str__(self):
    return self.date

  def __bytes__(self):
    return self.date.encode('utf-8')


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

  def __str__(self) -> str:
    return str(self.data)

  def __bytes__(self) -> bytes:
    return str(self.data).encode('utf-8')

  def __repr__(self) -> str:
    return f'{self.category}({self.data})'


@dataclass
class CommandPacket(Packet):
  category: str = field(init=False, default='CommandPacket')
  data: command_packet

  def __post_init__(self):
    self.auth_data = self.data.get('AUTH', {})
    self.game_data = self.data.get('GAME', {})

  def __str__(self) -> str:
    return str({'AUTH': self.auth_data, 'GAME': self.game_data})

  def __bytes__(self) -> bytes:
    return str({'AUTH': self.auth_data, 'GAME': self.game_data}).encode('utf-8')

  def __repr__(self) -> str:
    return f'{self.category}(AUTH={repr(self.auth_data)}, GAME={repr(self.game_data)})'

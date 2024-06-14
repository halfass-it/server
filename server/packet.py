import json

from server.commands import Commands

class Packet:
  def __init__(self, type: str) -> None:
    self.type = type

  def __str__(self) -> str:
    return ''

  def __repr__(self) -> str:
    return f"{self.type}()"


class DataPacket(Packet):
  def __init__(self, data: dict):
    super().__init__('DataPacket')
    self.data = data

  def __str__(self) -> str:
    return self.data

  def __bytes__(self) -> bytes:
    return self.data.encode('utf-8')

  def __repr__(self) -> str:
    return f"{self.type}({json.dumps(self.data)})"


class CommandPacket(Packet):
  def __init__(self, in_data) -> None:
    super().__init__('CommandPacket')
    self.in_data = in_data
    self.out_data = ""

  def process(self):
    self.out_data = Commands.process(self.in_data)

  def __str__(self) -> str:
    return json.dump(self.out_data)

  def __bytes__(self) -> bytes:
    return self.data.encode('utf-8')

  def __repr__(self) -> str:
    return f"{self.type}({json.dumps(self.out_data)}))"


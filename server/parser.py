import json
from dataclasses import dataclass

from utils.logger import Logger
from utils.packet import CommandPacket
from server.gateway import ServerGateway


@dataclass
class Parser:
  logger: Logger

  def input(self, data: bytes) -> CommandPacket:
    try:
      headers, json_data = data.decode('utf-8').split('\r\n\r\n', 1)
      self.logger.debug(f'[DEBUG] HTTP Headers: {", ".join(headers.splitlines())}')
      json_obj = json.loads(json_data)
      self.logger.debug(f'[DEBUG] JSON Data: {json_obj}')
      return CommandPacket(json_obj)
    except (json.JSONDecodeError, ValueError) as e:
      self.logger.error(f'[ERROR] Invalid JSON input: {e}')
      return None
    except Exception as e:
      self.logger.error(f'[ERROR] Parsing error in input: {e}')
      return None

  def output(self, packet: CommandPacket) -> CommandPacket:
    try:
      server_gateway: ServerGateway = ServerGateway()
      res_packet: CommandPacket = server_gateway.forward(packet, self.logger)
      return res_packet
    except Exception as e:
      self.logger.error(f'[ERROR] Parsing error in output: {e}')
      return ''.encode('utf-8')

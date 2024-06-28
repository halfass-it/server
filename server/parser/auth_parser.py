import json
from dataclasses import dataclass

from server.logger.logger import Logger
from server.types.ctypes import AuthPacket

from server.auth_server.auth import Auth


@dataclass
class Parser:
  auth: Auth
  logger: Logger

  def input(self, data: bytes) -> AuthPacket:
    try:
      headers, json_data = data.decode('utf-8').split('\r\n\r\n', 1)
      self.logger.error(f'{json_data}')
      self.logger.debug(f'[PARSER] HTTP Headers: {", ".join(headers.splitlines())}')
      json_obj = json.loads(json_data)
      self.logger.debug(f'[PARSER] JSON Data: {json_obj}')
      return AuthPacket(json_obj)
    except (json.JSONDecodeError, ValueError) as e:
      self.logger.error(f'[PARSER] Invalid JSON input: {e}')
      return AuthPacket({})
    except Exception as e:
      self.logger.error(f'[PARSER] Parsing error in input: {e}')
      return AuthPacket({})

  def filter(self, data: str) -> str:
    # TODO: add more filters and make it more robust
    return data.replace(' ', '').replace('\n', '').replace('\r', '')

  def output(self, auth_packet: AuthPacket) -> AuthPacket:
    try:
      username: str = self.filter(auth_packet.data['username'])
      token: str = self.filter(auth_packet.data['token'])
      command: str = self.filter(auth_packet.data['command'])
      if command == 'register':
        if self.auth.register(username, token, self.logger):
          return AuthPacket({ 'username': username, 'status': 'success'})
      elif command == 'login':
        if self.auth.login(username, token, self.logger):
          return AuthPacket({ 'username': username, 'status': 'success'})
      else:
        self.logger.error(f'[PARSER] Invalid command: {command}')
      return AuthPacket({ 'username': username, 'status': 'failure'})
    except Exception as e:
      self.logger.error(f'[PARSER] Parsing error in output: {e}')
      return AuthPacket({ 'username': username, 'status': 'failure'})

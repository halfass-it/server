from pathlib import Path
from dataclasses import dataclass
import asyncio
import json

from server.system.filesystem import CacheDir
from server.loggers.logger_to_file import LoggerToFile
from server.types.ctypes import Packet, GatewayPacket, AuthPacket, GamePacket


@dataclass
class Server:
  ip: str
  port: int
  buffer_size: int
  timeout: int
  cache_dir: Path = None
  server_class: str = 'generic'

  def __post_init__(
    self,
  ) -> None:
    self.cache_dir: Path = self.cache_dir if self.cache_dir else CacheDir().path
    self.logger = LoggerToFile(name=self.server_class, cache_dir=self.cache_dir)

  def decode(
    self, data: bytes, packet: Packet | GatewayPacket | AuthPacket | GamePacket
  ) -> Packet | GatewayPacket | AuthPacket | GamePacket:
    try:
      headers, json_data = data.decode('utf-8').split('\r\n\r\n', 1)
      self.logger.error(f'{json_data}')
      self.logger.debug(f'[{self.server_class.upper()}_SERVER] HTTP Headers: {", ".join(headers.splitlines())}')
      json_obj = json.loads(json_data)
      self.logger.debug(f'[{self.server_class.upper()}_SERVER] JSON Data: {json_obj}')
      if self.server_class == 'auth':
        return AuthPacket(json_obj)
      if self.server_class == 'gateway':
        return GatewayPacket(json_obj)
      if self.server_class == 'game':
        return GamePacket(json_obj)
      return Packet({})
    except (json.JSONDecodeError, ValueError) as e:
      self.logger.error(f'[{self.server_class.upper()}_SERVER] Invalid JSON input: {e}')
      return Packet({})
    except Exception as e:
      self.logger.error(f'[{self.server_class.upper()}_SERVER] Parsing error in input: {e}')
      return Packet({})

  def eval(
    self, upstream_packet: Packet | GatewayPacket | AuthPacket | GamePacket
  ) -> Packet | GatewayPacket | AuthPacket | GamePacket:
    return upstream_packet

  async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    client_ip, client_port = writer.get_extra_info('peername')
    self.logger.info(
      f'[{self.server_class.upper()}_SERVER] Connected from {client_ip}:{client_port} to client {self.ip}:{self.port}'
    )
    try:
      while True:
        upstream_data: bytes = await asyncio.wait_for(reader.read(self.buffer_size), timeout=self.timeout)
        if not upstream_data:
          self.logger.info(f'[{self.server_class.upper()}_SERVER] Client closed the connection')
          break
        upstream_packet: Packet | GatewayPacket | AuthPacket | GamePacket = self.decode(upstream_data)
        try:
          self.logger.info(
            f"[{self.server_class.upper()}_SERVER]: '{upstream_packet.data}' from {client_ip}:{client_port}"
          )
          downstream_packet: Packet | GatewayPacket | AuthPacket | GamePacket = self.eval(upstream_packet)
          downstream_data: bytes = bytes(downstream_packet)
        except Exception as e:
          self.logger.error(f'[{self.server_class.upper()}_SERVER] Error processing client data: {e}')
          break
        writer.write(downstream_data)
        await writer.drain()
        self.logger.info(f'[{self.server_class.upper()}_SERVER]: {downstream_packet.data} to {client_ip}:{client_port}')
        break
    except asyncio.TimeoutError:
      self.logger.error(f'[{self.server_class.upper()}_SERVER] Connection timeout for {client_ip}:{client_port}')
    except Exception as e:
      self.logger.error(f'[{self.server_class.upper()}_SERVER] Unexpected error handling client data: {e}')
    finally:
      try:
        writer.close()
        await writer.wait_closed()
      except Exception as e:
        self.logger.error(f'[{self.server_class.upper()}_SERVER] Error closing connection: {e}')
      self.logger.info(f'[{self.server_class.upper()}_SERVER] Disconnected from {client_ip}:{client_port}')

  async def start(self) -> None:
    try:
      server = await asyncio.start_server(self.handle_client, self.ip, self.port)
      self.logger.info(f'[{self.server_class.upper()}_SERVER] Server started on {self.ip}:{self.port}')
      async with server:
        await server.serve_forever()
    except Exception as e:
      self.logger.error(f'[{self.server_class.upper()}_SERVER] Failed to start server: {e}')
    finally:
      self.logger.info(f'[{self.server_class.upper()}_SERVER] Server stopped on {self.ip}:{self.port}')

  def run(self) -> None:
    asyncio.run(self.start())

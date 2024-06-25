from pathlib import Path
from dataclasses import dataclass
import asyncio

from utils.filesystem import CacheDir
from utils.logger_to_file import LoggerToFile
from utils.packet import AuthPacket
from .parser import Parser
from .auth import Auth


@dataclass
class AuthServer:
  ip: str
  port: int
  buffer_size: int
  timeout: int
  cache_dir: Path = None

  def __post_init__(
    self,
  ) -> None:
    print('AUTH_SERVER')
    exit(0)
    self.cache_dir: Path = self.cache_dir if self.cache_dir else CacheDir().path
    self.logger = LoggerToFile(name='auth_server', cache_dir=self.cache_dir)
    self.auth = Auth()
    # TODO: is this required for multiprocess logging to work or is it dreadlocked by default?
    # import time
    # time.sleep(0.5)
    self.parser = Parser(auth=self.auth, logger=self.logger)

  async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    client_ip, client_port = writer.get_extra_info('peername')
    self.logger.info(f'[AUTH_SERVER] Connected to client from {client_ip}:{client_port} at {self.ip}:{self.port}')
    try:
      while True:
        upstream_data: bytes = await asyncio.wait_for(reader.read(self.buffer_size), timeout=self.timeout)
        if not upstream_data:
          self.logger.info('[AUTH_SERVER] Client closed the connection')
          break
        in_packet: AuthPacket = self.parser.input(upstream_data)
        try:
          self.logger.info(f"[AUTH_SERVER]: '{in_packet.data}' from {client_ip}:{client_port}")
          out_packet: AuthPacket = self.parser.output(in_packet)
          downstream_data: bytes = bytes(out_packet)
        except Exception as e:
          self.logger.error(f'[AUTH_SERVER] Error processing client data: {e}')
          break
        writer.write(downstream_data)
        await writer.drain()
        self.logger.info(f'[AUTH_SERVER]: {out_packet.data} to {client_ip}:{client_port}')
        break
    except asyncio.TimeoutError:
      self.logger.error(f'[AUTH_SERVER] Connection timeout for {client_ip}:{client_port}')
    except Exception as e:
      self.logger.error(f'[AUTH_SERVER] Unexpected error handling client data: {e}')
    finally:
      try:
        writer.close()
        await writer.wait_closed()
      except Exception as e:
        self.logger.error(f'[AUTH_SERVER] Error closing connection: {e}')
      self.logger.info(f'[AUTH_SERVER] Disconnected from {client_ip}:{client_port}')

  async def start(self):
    try:
      server = await asyncio.start_server(self.handle_client, self.ip, self.port)
      self.logger.info(f'[AUTH_SERVER] Server started on {self.ip}:{self.port}')
      async with server:
        await server.serve_forever()
    except Exception as e:
      self.logger.error(f'[AUTH_SERVER] Failed to start server: {e}')
    finally:
      self.logger.info(f'[AUTH_SERVER] Server stopped on {self.ip}:{self.port}')

  def run(self):
    asyncio.run(self.start())

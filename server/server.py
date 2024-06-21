from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import asyncio

from utils.filesystem import CacheDir
from utils.logger_to_file import LoggerToFile
from utils.packet import CommandPacket
from server.parser import Parser


@dataclass
class Server:
  ip: str
  port: int
  buffer_size: int
  timeout: int
  cache_dir: Optional[Path] = None

  def __post_init__(
    self,
  ) -> None:
    self.cache_dir: Path = self.cache_dir if not self.cache_dir else CacheDir().path
    self.logger = LoggerToFile(cache_dir=self.cache_dir)
    self.parser = Parser(logger=self.logger)

  async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    client_ip, client_port = writer.get_extra_info('peername')
    self.logger.info(f'[OPENED] Connected to client from {client_ip}:{client_port} at {self.ip}:{self.port}')
    try:
      while True:
        upstream_data: bytes = await asyncio.wait_for(reader.read(self.buffer_size), timeout=self.timeout)
        if not upstream_data:
          self.logger.info('[CLOSED] Client closed the connection')
          break
        in_packet: CommandPacket = self.parser.input(upstream_data)
        try:
          self.logger.info(f"[UPSTREAM]: '{in_packet.data}' from {client_ip}:{client_port}")
          out_packet: CommandPacket = self.parser.output(in_packet)
          downstream_data: bytes = bytes(out_packet)
        except Exception as e:
          self.logger.error(f'[ERROR] Error processing client data: {e}')
          break
        writer.write(downstream_data)
        await writer.drain()
        self.logger.info(f'[DOWNSTREAM]: {out_packet.data} to {client_ip}:{client_port}')
        break
    except asyncio.TimeoutError:
      self.logger.error(f'[ERROR] Connection timeout for {client_ip}:{client_port}')
    except Exception as e:
      self.logger.error(f'[ERROR] Unexpected error handling client data: {e}')
    finally:
      try:
        writer.close()
        await writer.wait_closed()
      except Exception as e:
        self.logger.error(f'[ERROR] Error closing connection: {e}')
      self.logger.info(f'[CLOSED] Disconnected from {client_ip}:{client_port}')

  async def start(self):
    try:
      server = await asyncio.start_server(self.handle_client, self.ip, self.port)
      self.logger.info(f'[START] Server started on {self.ip}:{self.port}')
      async with server:
        await server.serve_forever()
    except Exception as e:
      self.logger.error(f'[ERROR] Failed to start server: {e}')
    finally:
      self.logger.info(f'[STOP] Server stopped on {self.ip}:{self.port}')

  def run(self):
    asyncio.run(self.start())

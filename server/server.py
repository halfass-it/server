import asyncio
from pathlib import Path
import memcache
from typing import Optional
from utils.filesystem import CacheDir
from utils.logger_to_file import LoggerToFile
from utils.packet import Packet, CommandPacket
from server.parser import Parser


class Server:
  def __init__(
    self,
    ip: str,
    port: int,
    buffer_size: int,
    timeout: int,
    cache_dir: Optional[Path] = None,
  ) -> None:
    self.ip: str = ip
    self.port: int = port
    self.buffer_size: int = buffer_size
    self.timeout: int = timeout
    self.cache_dir: Path = cache_dir or CacheDir().path
    self.mc = memcache.Client(['127.0.0.1:11211'])
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
        try:
          packet: CommandPacket = self.parser.input(upstream_data)
          self.logger.info(f"[UPSTREAM]: '{packet.data}' from {client_ip}:{client_port}")
          command_packet: CommandPacket = self.parser.output(packet)
        except Exception as e:
          self.logger.error(f'[ERROR] Error processing client data: {e}')
          break
        downstream_data: bytes = bytes(command_packet)
        writer.write(downstream_data)
        await writer.drain()
        self.logger.info(f'[DOWNSTREAM]: {command_packet.data} to {client_ip}:{client_port}')
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

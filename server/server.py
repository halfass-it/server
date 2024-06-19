import asyncio
from pathlib import Path

import memcache

from utils.filesystem import CacheDir
from utils.logger_to_file import LoggerToFile
from server.parser import Parser
from server.packet import Packet, CommandPacket


class Server:
  def __init__(self, ip: str, port: int, buffer_size: int, timeout: int, cache_dir: Path = None) -> None:
    self.ip: str = ip
    self.port: int = port
    self.buffer_size: int = buffer_size
    self.timeout: int = timeout
    self.cache_dir: Path = CacheDir() if not cache_dir else cache_dir
    self.mc = memcache.Client(['127.0.0.1:11211'])
    # self.mc.set('key', 'value') | value = self.mc.get('key')
    # TODO: add memcache to store data properly
    self.logger = LoggerToFile(cache_dir=self.cache_dir)
    self.parser = Parser(logger=self.logger, cache_dir=self.cache_dir)

  async def handle_client(self, reader, writer):
    client_ip, client_port = writer.get_extra_info('peername')
    self.logger.info(f'[OPENED] Connected to client from {client_ip}:{client_port} at {self.ip}:{self.port}')
    try:
      while True:
        upstream_data: bytes = await reader.read(self.buffer_size)
        if not upstream_data:
          self.logger.info('[CLOSED] Client closed the connection')
          break
        try:
          packet: Packet = self.parser.input(upstream_data)
          self.logger.info(f"[UPSTREAM]: '{packet.data}' from {client_ip}:{client_port}")
        except Exception as e:
          self.logger.error(f'[ERROR] Error handling client data, closing connection: {e}')
          break
        try:
          command_packet: CommandPacket = self.parser.output(packet)
        except Exception as e:
          self.logger.error(f'[ERROR] Error handling client data, closing connection: {e}')
          break
        finally:
          if not command_packet:
            self.logger.info('[CLOSED] Client packet is corrupted')
            break
          downstream_data: bytes = bytes(command_packet)
          writer.write(downstream_data)
          await writer.drain()
          self.logger.info(f"[DOWNSTREAM]: '{packet.data}' to {client_ip}:{client_port}")
          break
    except Exception as e:
      self.logger.error(f'[ERROR] Error handling client data, closing connection\n[STACKTRACE]: {e}')
    finally:
      try:
        writer.close()
        await writer.wait_closed()
        self.logger.info(f'[CLOSED] Disconnected from {client_ip}:{client_port}')
      except Exception as e:
        self.logger.error(f'[ERROR] Error closing connection\n[STACKTRACE]: {e}')

  async def start(self):
    server = await asyncio.start_server(self.handle_client, self.ip, self.port)
    async with server:
      self.logger.info(f'[START] Server started on {self.ip}:{self.port}')
      await server.serve_forever()
    self.logger.info(f'[STOP] Server stopped on {self.ip}:{self.port}')

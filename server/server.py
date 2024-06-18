import asyncio
import json
from pathlib import Path

from utils.filesystem import CacheDir
from utils.logger import Logger
from server.packet import CommandPacket


class Server:
  def __init__(self, ip: str, port: int, buffer_size: int, timeout: int, cache_dir: Path = None) -> None:
    self.ip: str = ip
    self.port: int = port
    self.buffer_size: int = buffer_size
    self.timeout: int = timeout
    name: str = str(__name__.split('.')[-1])
    logs_dir: Path = Path(str(CacheDir())) / 'logs' if not cache_dir else cache_dir
    self.logger: Logger = Logger(name=name, logs_dir=logs_dir)()

  async def handle_client(self, reader, writer):
    client_ip, client_port = writer.get_extra_info('peername')
    self.logger.info(f'[OPENED] Connected to client from {client_ip}:{client_port} at {self.ip}:{self.port}')

    try:
      while True:
        data = await reader.read(self.buffer_size)
        if not data:
          self.logger.info('[CLOSED] Client closed the connection.')
          break
        packet = self.process_input(data)
        self.logger.info(f"[UPSTREAM]: '{packet.in_data}' from {client_ip}:{client_port}")
        response_data = self.process_output(packet)
        writer.write(response_data)
        await writer.drain()
        self.logger.info(f"[DOWNSTREAM]: '{packet.out_data}' to {client_ip}:{client_port}")
        break
    except Exception as e:
      self.logger.error(f'[ERROR] Error handling client data, closing connection... stracktrace: {e}')
    finally:
      writer.close()
      await writer.wait_closed()
      self.logger.info(f'[CLOSED] Disconnected from {client_ip}:{client_port}')

  def process_input(self, data: bytes) -> CommandPacket:
    try:
      # Decode bytes to string and split headers from body
      decoded_data = data.decode('utf-8')
      headers, json_data = decoded_data.split('\r\n\r\n', 1)
      self.logger.debug(f'[DEBUG] HTTP Headers: {headers}') 
      json_obj = json.loads(json_data)
      if 'data' not in json_obj:
        raise ValueError("[ERROR] JSON does not contain 'data' field")

      return CommandPacket(json_obj['data'])
    except (json.JSONDecodeError, ValueError) as e:
      self.logger.error(f'[ERROR] Invalid JSON received: {e}')
      raise
    except Exception as e:
      self.logger.error(f'[ERROR] Unexpected error: {e}')
      raise

  def process_output(self, packet: CommandPacket) -> bytes:
    packet.process()
    return json.dumps({'data': packet.out_data}).encode('utf-8')

  async def start(self):
    server = await asyncio.start_server(self.handle_client, self.ip, self.port)
    async with server:
      self.logger.info(f'Server started on {self.ip}:{self.port}')
      await server.serve_forever()

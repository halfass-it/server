import asyncio
from pathlib import Path

from utils.filesystem import CacheDir
from utils.logger import Logger
from server.parser import Parser

class Server:
    def __init__(self, ip: str, port: int, buffer_size: int, timeout: int, cache_dir: Path = None) -> None:
        self.ip: str = ip
        self.port: int = port
        self.buffer_size: int = buffer_size
        self.timeout: int = timeout
        self.cache_dir: Path = cache_dir

        self.logger = self._build_logger(self.cache_dir)
        self.parser = self._build_parser(self.logger, self.cache_dir)

    def _build_logger(self, cache_dir: Path = None) -> Logger:
        name: str = str(__name__.split('.')[-1])
        logs_dir: Path = Path(str(CacheDir())) / \
            'logs' if not cache_dir else cache_dir / 'logs'
        return Logger(name=name, logs_dir=logs_dir)()

    def _build_parser(self, logger: Logger, cache_dir: Path = None) -> Parser:
        return Parser(logger=logger, cache_dir=cache_dir)

    async def handle_client(self, reader, writer):
        client_ip, client_port = writer.get_extra_info('peername')
        self.logger.info(f'[OPENED] Connected to client from {client_ip}:{client_port} at {self.ip}:{self.port}')

        try:
            while True:
                data = await reader.read(self.buffer_size)
                if not data:
                    self.logger.info('[CLOSED] Client closed the connection')
                    break
                packet = self.parser.process_input(data)
                self.logger.info(f"[UPSTREAM]: '{packet.data}' from {client_ip}:{client_port}")
                response_data = self.parser.process_output(packet)
                if not response_data:
                    self.logger.info('[CLOSED] Client packet is corrupted')
                    break
                writer.write(response_data)
                await writer.drain()
                self.logger.info(f"[DOWNSTREAM]: '{packet.data}' to {client_ip}:{client_port}")
                break
        except Exception as e:
            self.logger.error(f'[ERROR] Error handling client data, closing connection\n[STACKTRACE]: {e}')
        finally:
            writer.close()
            await writer.wait_closed()
            self.logger.info(f'[CLOSED] Disconnected from {client_ip}:{client_port}')

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.ip, self.port)
        async with server:
            self.logger.info(f'[START] Server started on {self.ip}:{self.port}')
            await server.serve_forever()
        self.logger.info(f'[STOP] Server stopped on {self.ip}:{self.port}')

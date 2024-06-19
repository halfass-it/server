
import json
from pathlib import Path

from utils.logger import Logger
from server.packet import CommandPacket
from server.gateway import ServerGateway


class Parser:
    def __init__(self, logger: Logger, cache_dir: Path) -> None:
        self.cache_dir = cache_dir
        self.logger = logger

    def process_input(self, data: bytes) -> CommandPacket:
        try:
            headers, json_data = data.decode('utf-8').split('\r\n\r\n', 1)
            self.logger.debug(f'[DEBUG] HTTP Headers: {headers}')
            json_obj = json.loads(json_data)
            self.logger.debug(f'[DEBUG] JSON Data: {json_obj}')
            return CommandPacket(json_obj)
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error(f'[ERROR] Invalid JSON received: {e}')
            raise
        except Exception as e:
            self.logger.error(f'[ERROR] Unexpected error: {e}')
            raise

    def process_output(self, packet: CommandPacket) -> bytes:
        try:
          ServerGateway.evaluate(packet)
        except Exception as e:
            self.logger.error(f'[ERROR] Unexpected error: {e}')
            return ''.encode('utf-8')
        return json.dumps({'data': packet.data}).encode('utf-8')

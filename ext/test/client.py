import socket
from dataclasses import dataclass

IP: str = '127.0.0.1'
PORT: int = 4242
BUFFER: int = 1024


@dataclass
class Logger:
  def log(self, data):
    print(data)


@dataclass
class Client:
  def __post_init__(self):
    self.logger = Logger()
    try:
      self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
      self.logger.log(f'Error creating socket: {e}')
      exit(1)

  def send(self, data: str) -> int:
    try:
      self.conn.sendto(data.encode(), (IP, PORT))
      self.conn.settimeout(1)
    except socket.timeout:
      self.logger.log(f"Timeout sending: '{data}' to {IP}:{PORT}")
      return 1
    self.logger.log(f"Sent: '{data}' to {IP}:{PORT}")
    return 0

  def recv(self) -> str:
    try:
      data, (recv_ip, recv_port) = self.conn.recvfrom(BUFFER)
      data = data.decode()
      self.logger.log(f"Received: '{data}' from {recv_ip}:{recv_port}")
    except socket.timeout:
      self.logger.log(f'Timeout receiving from {IP}:{PORT}')
      return ''
    return data if data else ''


def test_client():
  client = Client()
  client.send('ping')
  assert client.recv() == 'pong'
  client.send('Success!')
  assert client.recv() == 'invalid'


def main():
  test_client()


if __name__ == '__main__':
  main()
  exit(0)

import sys

from jsonargparse import CLI

from server.client import Client


class Main:
  def __init__(self, ip: str, port: str, buffer_size: str, timeout: str) -> None:
    self.ip: str = ip
    self.port: int = int(port)
    self.buffer_size: int = int(buffer_size)
    self.timeout: int = int(timeout)

  def run(self):
    client = Client(self.ip, self.port, self.buffer_size, self.timeout)
    client.listen()
    client.close()


def main():
  try:
    CLI(Main)
    return 0
  except KeyboardInterrupt:
    return 0
  except ValueError:
    return 0


if __name__ == '__main__':
  main()
  sys.exit(main())

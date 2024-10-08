import sys

from jsonargparse import CLI

from server.server.game_server import GameServer


class Main:
  def __init__(
    self,
    ip: str,
    port: str,
    buffer_size: str,
    timeout: str,
    cache_dir: str,
  ) -> None:
    self.ip: str = ip
    self.port: int = int(port)
    self.buffer_size: int = int(buffer_size)
    self.timeout: int = int(timeout)
    self.cache_dir: str = cache_dir

  def run(self):
    GameServer(
      self.ip,
      self.port,
      self.buffer_size,
      self.timeout,
      self.cache_dir,
    ).run()


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

import sys

from twisted.python import log
from twisted.internet import reactor, task
from autobahn.twisted.websocket import WebSocketServerFactory

from server.protocol import ServerProtocol


class GameFactory(WebSocketServerFactory):
  def __init__(self, hostname: str, port: int):
    self.protocol = ServerProtocol
    super().__init__(f'ws://{hostname}:{port}')

    self.clients: set[ServerProtocol] = set()

    tickloop = task.LoopingCall(self.tick)
    tickloop.start(1 / 20)  # 20 times per second

  def tick(self):
    for p in self.clients:
      p.tick()

  def buildProtocol(self, addr):
    p = super().buildProtocol(addr)
    self.clients.add(p)
    return p


def main():
  log.startLogging(sys.stdout)

  HOSTNAME: str = '127.0.0.1'
  PORT: int = 8080

  factory = GameFactory(HOSTNAME, PORT)

  reactor.listenTCP(PORT, factory)
  reactor.run()


if __name__ == '__main__':
  main()
  exit(0)

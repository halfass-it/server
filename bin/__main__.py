from jsonargparse import CLI

from server.client import Client


class Main:
  def run(self):
    client = Client(ip='127.0.0.1', port=2001, buffer_size=1024, timeout=60)
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
  exit(main())

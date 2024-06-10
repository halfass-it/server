from server.client import Client

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

#!/usr/bin/env python3

import socket
import json
import time
import statistics

AUTH_PACKET = {
    'USERNAME': '$USERNAME',
    'TOKEN': '$AUTH_TOKEN',
    'COMMAND': '$AUTH_COMMAND'
}

GAME_PACKET = {
    'TOKEN': '$GAME_TOKEN',
    'COMMAND': '$GAME_COMMAND'
}

GATEWAY_PACKET = {
    'AUTH': AUTH_PACKET,
    'GAME': GAME_PACKET
}

GATEWAY_PORT = 5000
AUTH_PORT = 6000
GAME_PORT = 7000


def fuzz(port, packet):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = ('localhost', port)
  sock.connect(server_address)
  print(f'[+] {server_address}')
  try:
    message = json.dumps(packet)
    request = (
      f'POST / HTTP/1.1\r\n'
      f'Host: localhost\r\n'
      f'Content-Type: application/json\r\n'
      f'Content-Length: {len(message)}\r\n'
      f'User-Agent: HALFASS\r\n'  # Adding User-Agent header
      f'\r\n'
      f'{message}'
    )
    print(f'[>] {request}')
    sock.sendall(request.encode('utf-8'))
    response = sock.recv(4096)
    print(f'[<] {response.decode("utf-8")}')
  finally:
    print('[-] Closing socket')
    sock.close()


def monitor_fuzzer(number_requests, port, packet):
  timings = []
  for i in range(number_requests):
    start_time = time.time()
    fuzz(port, packet)
    end_time = time.time()
    elapsed_time = end_time - start_time
    timings.append(elapsed_time)
    print(f'[!] Round: {i + 1} \n[!] Time: {elapsed_time:.6f} seconds')
  median_time = statistics.median(timings)
  mean_time = statistics.mean(timings)
  total_time = sum(timings)
  max_time = max(timings)
  min_time = min(timings)
  print('\n[!] Performance Metrics:')
  print(f'[!] Requests: {number_requests}')
  print(f'[!] Median Time: {median_time:.6f} seconds')
  print(f'[!] Mean Time: {mean_time:.6f} seconds')
  print(f'[!] Total Time: {total_time:.6f} seconds')
  print(f'[!] Max Time: {max_time:.6f} seconds')
  print(f'[!] Min Time: {min_time:.6f} seconds')


if __name__ == '__main__':
  number_requests = 1
  port = GATEWAY_PORT
  packet = GATEWAY_PACKET
  monitor_fuzzer(number_requests)

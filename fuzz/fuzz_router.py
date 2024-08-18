#!/usr/bin/env python3

import socket
import ssl
import json
import time
import statistics


PACKET = {
  'AUTH': {
    'username': '$USERNAME',
    'token': '$AUTH_TOKEN',
    'command': '$AUTH_COMMAND',
  },
  'GAME': {'token': '$GAME_TOKEN', 'command': '$GAME_COMMAND'},
}


def fuzz():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  context = ssl.create_default_context()
  context.check_hostname = False
  context.verify_mode = ssl.CERT_NONE
  wrapped_sock = context.wrap_socket(sock, server_hostname='localhost')
  server_address = ('localhost', 443)
  print(f'[+] {server_address}')
  wrapped_sock.connect(server_address)
  try:
    message = json.dumps(PACKET)
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
    wrapped_sock.sendall(request.encode())
    response = wrapped_sock.recv(4096)
    print(f'[<] {response.decode()}')
  finally:
    print('[-] Closing socket')
    wrapped_sock.close()


def monitor_fuzzer(number_requests):
  timings = []
  for i in range(number_requests):
    start_time = time.time()
    fuzz()
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
  monitor_fuzzer(number_requests)

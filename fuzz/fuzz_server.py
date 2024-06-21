#!/usr/bin/env python3

import socket
import json
import time
import statistics

PACKET = {
  'AUTH': {'TOKEN': '$TOKEN', 'USERNAME': '$USERNAME'},
  'GAME': {'ACTION': '$ACTION', 'DATA': '$DATA'},
}


def fuzz():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = ('localhost', 1337)
  sock.connect(server_address)
  print(f'[+] {server_address}')
  try:
    message = json.dumps(PACKET)
    request = f'POST / HTTP/1.1\r\nHost: localhost\r\nContent-Type: application/json\r\nContent-Length: {len(message)}\r\n\r\n{message}'
    print(f'[>] {request}')
    sock.sendall(request.encode('utf-8'))
    response = sock.recv(4096)
    print(f'[<] {response.decode("utf-8")}')
  finally:
    print('[-] Closing socket')
    sock.close()


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

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))
s.send(b'GET / HTTP/1.1\r\nHost: 127.0.0.1:8000\r\nConnection: close\r\n\r\n')

data = b''
while True:
    chunk = s.recv(1024)
    if not chunk:
        break
    data += chunk

print('Total length:', len(data))
print('Response:', data[:500])
s.close()

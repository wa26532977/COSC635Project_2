import socket
import pickle

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 5006))


while True:
    data, addr = sock.recvfrom(4096)
    print(f'{pickle.loads(data)}')
    msg = "Welcome To The server"
    msg = f'{len(msg):<10}' + msg
    sock.sendto(bytes(msg, 'utf-8'), addr)



import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("127.0.0.1", 5005)
sock.bind(address)

while True:
    data, addr = sock.recvfrom(4096)
    print(data)
    message = "Hello I am your server".encode('UTF-8')
    sock.sendto(message, addr)

import socket


class Receiver:

    def __init__(self, addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((addr, port))

    def start_listening(self):
        stop_listen = False
        while not stop_listen:
            data, addr = self.sock.recvfrom(4096)
            pack_string = data.decode('UTF-8')
            print(pack_string)
            first_comma = pack_string.find(",")
            print(pack_string[:first_comma])

            message = pack_string[:first_comma].encode('UTF-8')
            self.sock.sendto(message, addr)


if __name__ == '__main__':
    receiver_1 = Receiver("127.0.0.1", 5005)
    receiver_1.start_listening()


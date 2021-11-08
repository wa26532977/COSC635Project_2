import socket
import pickle


class ClientServer:
    def __init__(self, pock_lost, msg, addr, port):
        self.pocket_lost = pock_lost
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.msg = msg.encode('UTF-8')
        self.msg = msg
        self.addr = addr
        self.port = port


    def client_sent(self):
        print(f"pocket_lost: {self.pocket_lost}")
        self.client_socket.sendto(self.msg, (self.addr, self.port))
        data, addr = self.client_socket.recvfrom(4096)
        print('Server Says:')
        print(str(data))

    def close_socket(self):
        self.client_socket.close()


# this for testing
if __name__ == '__main__':
    # split in to bytes
    # i = 0
    # with open("DataSent.txt", "r", encoding="utf8") as in_file:
    #     bytes = in_file.read(88)  # read 5000 bytes
    #     while bytes:
    #         with open("split_into_small/out-file-" + str(i), 'w', encoding="utf8") as output:
    #             output.write(" ".join(format(ord(x), 'b') for x in bytes))
    #         bytes = in_file.read(88)  # read another 5000 bytes
    #         i += 1

    while True:
        pocket_lost = input("Please enter pocket_lost number between 0-99:")
        try:
            if 0 < int(pocket_lost) < 99:
                break
        except:
            print(f"{pocket_lost} is not a number between 0-99")

    i = 0
    with open("DataSent.txt", "r", encoding="utf8") as in_file:
        bytes = in_file.read(300)  # read 5000 bytes
        while bytes:
            with open("split_into_small/out-file-" + str(i), 'w', encoding="utf8") as output:
                msg = bytes.encode('UTF-8')
                client_1 = ClientServer(pocket_lost, msg, '127.0.0.1', 5005)
                client_1.client_sent()
            bytes = in_file.read(3000)  # read another 5000 bytes
            i += 1
        client_1.close_socket()




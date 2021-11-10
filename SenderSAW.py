import socket
import numpy as np
import time
from random import randrange


class ClientServer:
    def __init__(self, pock_lost, msg, addr, port):
        self.pocket_lost = pock_lost
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.msg = msg.encode('UTF-8')
        self.msg = msg
        self.addr = addr
        self.port = port
        self.pack_number = ''
        self.connection_fail = 0

    def client_sent(self, good_pack_number):
        random_number = randrange(99)
        print(f"pocket_lost: {self.pocket_lost} and random number is {random_number}")
        print(random_number)
        if random_number > int(self.pocket_lost):
            self.client_socket.sendto(self.msg, (self.addr, self.port))
        try:
            time.sleep(1)
            data, addr = self.client_socket.recvfrom(4096)
            print(f'Server Says: {str(data)}')
            self.pack_number = data.decode('UTF-8')
        except:
            print("bad connection")
            self.connection_fail += 1
            print(f"connection fail {self.connection_fail}")
            time.sleep(1)
            self.client_sent(good_pack_number)

        if good_pack_number != self.pack_number:
            self.client_sent(good_pack_number)

    def close_socket(self):
        self.client_socket.close()


# this for testing
if __name__ == '__main__':

    while True:
        pocket_lost = input("Please enter pocket_lost number between 0-99:")
        try:
            if 0 < int(pocket_lost) < 99:
                break
        except:
            print(f"{pocket_lost} is not a number between 0-99")
    #

    total_pack_lost = 0
    i = 0
    with open("DataSent.txt", "r", encoding="utf8") as in_file:
        bytes = in_file.read(3000)  # read 5000 bytes
        while bytes:
            if i < 5:
                with open("split_into_small/out-file-" + str(i), 'w', encoding="utf8") as output:
                    # print(bytes)
                    # print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~Part: {i}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                    msg = bytes.encode('UTF-8')
                    client_1 = ClientServer(pocket_lost, f"part_{i},".encode('UTF-8')+msg, '127.0.0.1', 5005)
                    client_1.client_sent(f"part_{i}")
                    total_pack_lost += client_1.connection_fail
                bytes = in_file.read(3000)  # read another 5000 bytes
                i += 1
            else:
                break
        client_1.close_socket()
    print(f"The pack was lost this name times {total_pack_lost}.")







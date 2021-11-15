import socket
import time
from random import randrange
import sys
import math
import pickle


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
        # create fake pack lost
        if random_number > int(self.pocket_lost):
            self.client_socket.sendto(self.msg, (self.addr, self.port))

        start_timer = time.time()
        # wait for receiver ack
        while time.time() - start_timer < 3:
            try:
                data, addr = self.client_socket.recvfrom(4096)
                print(f'Server Says: {str(data)}')
                self.pack_number = data.decode('UTF-8')
                # matching pack number
                if good_pack_number != self.pack_number:
                    self.client_sent(good_pack_number)
                return
            except:
                time.sleep(0.5)
                print("waiting....")

        print("bad connection")
        self.connection_fail += 1
        print(f"connection fail {self.connection_fail}")
        self.client_sent(good_pack_number)

    def close_socket(self):
        self.client_socket.close()


# this for testing
if __name__ == '__main__':
    pack_size = 3000
    while True:
        pocket_lost = input("Please enter pocket_lost number between 0-99:")
        try:
            if 0 < int(pocket_lost) < 99:
                break
        except:
            print(f"{pocket_lost} is not a number between 0-99")
    # find binary size of the txt file
    file = open("COSC635_P2_DataSent.txt", "r", encoding="utf8")
    total_pack = int(math.ceil(sys.getsizeof(file.read()) / pack_size))

    total_pack_lost = 0
    i = 1
    with open("COSC635_P2_DataSent.txt", "r", encoding="utf8") as in_file:
        bytes = in_file.read(pack_size)  # read 5000 bytes
        while bytes:
            msg_pickle = pickle.dumps({"part": i, "total_pack": total_pack, "msg": bytes})
            client_1 = ClientServer(pocket_lost, msg_pickle, '127.0.0.1', 5005)
            client_1.client_sent(f"part: {i}")
            total_pack_lost += client_1.connection_fail
            bytes = in_file.read(pack_size)  # read another 5000 bytes
            i += 1
        client_1.close_socket()
    print("Summery:")
    print(f"Total package send: {total_pack}")
    print(f"Each package size: {pack_size} bytes")
    print(f"Package Lost rate: {pocket_lost}%")
    print(f"The pack was lost: {total_pack_lost} times .")







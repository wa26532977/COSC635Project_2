import socket
import time
from random import randrange
import sys
import math
import pickle


class ClientServer:
    def __init__(self, pock_lost, all_massage, win_size, addr, port):
        self.pocket_lost = pock_lost
        self.window_size = int(win_size)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(0.1)
        self.all_msg = all_massage
        self.ack_pack_number = 0
        self.ack_list = []
        self.total_pack_number = len(all_massage)
        self.addr = addr
        self.port = port
        self.pack_number = ''
        self.connection_fail = 0

    def pocket_sent(self):
        random_number = randrange(99)
        print(f"random number: {self.pocket_lost} and random number is {random_number}")
        if random_number > int(self.pocket_lost):
            print("pocket_send")
            return True
        print("pocket_lost")
        return False

    def check_group_response(self):
        print(f"len ack_list: {len(self.ack_list)}")
        print(f"two number +: {self.ack_pack_number + self.window_size}")
        # check if 'out of order was in self.ack_list
        out_of_order = any('out of order' in string for string in self.ack_list)
        # this mean all the data was successfully send
        if len(self.ack_list) == (self.ack_pack_number + self.window_size) and not out_of_order:
            print("good one")
            self.ack_pack_number = len(self.ack_list)
            self.client_sent_group_pack()
            return
        # dont have out of orde by len of ack_list is short
        elif len(self.ack_list) < (self.ack_pack_number + self.window_size) and not out_of_order:
            self.ack_pack_number = len(self.ack_list)
            self.connection_fail += 1
            self.client_sent_group_pack()
            pass

        for n in self.ack_list:
            if "out of order" in n:
                self.connection_fail += 1
                print(n[31:])
                self.ack_list = self.ack_list[:int(n[31:])-1]
                print(self.ack_list)
                if len(self.ack_list) == 0:
                    self.client_sent_group_pack()
                else:
                    self.ack_pack_number = len(self.ack_list)
                    self.client_sent_group_pack()
                break

    def client_sent_group_pack(self):
        # this is for last pack if pack size is smaller then window size
        print("print from client sent group pack")
        if len(self.ack_list) + self.window_size > self.total_pack_number:
            self.window_size = self.total_pack_number - len(self.ack_list)
            if self.window_size == 0:
                return
            print(f"new window size {self.window_size}")
            print(f"len ack_list: {self.ack_list} ")

        for n in range(self.window_size):
            print(f"n: {self.ack_pack_number + n}")
            if self.pocket_sent():
                msg = self.all_msg[self.ack_pack_number + n]
                # print(pickle.loads(msg))
                self.client_socket.sendto(msg, (self.addr, self.port))

            try:
                data, addr = self.client_socket.recvfrom(4096)
                print(f'Server Says: {pickle.loads(data)}')
                self.ack_list.append(pickle.loads(data))
                # self.pack_number = data.decode('UTF-8')
            except:
                print("No response")
        print(f"ack list: {self.ack_list}")
        self.check_group_response()
        # all package send

    # def client_sent(self, msg, good_pack_number):
    #     random_number = randrange(99)
    #     print(f"pocket_lost: {self.pocket_lost} and random number is {random_number}")
    #     print(random_number)
    #     # create fake pack lost
    #     if random_number > int(self.pocket_lost):
    #         self.client_socket.sendto(msg, (self.addr, self.port))
    #
    #     start_timer = time.time()
    #     # wait for receiver ack
    #     while time.time() - start_timer < 3:
    #         try:
    #             print(time.time() - start_timer)
    #             data, addr = self.client_socket.recvfrom(4096)
    #             print(f'Server Says: {str(data)}')
    #             self.pack_number = data.decode('UTF-8')
    #             # matching pack number
    #             if good_pack_number != self.pack_number:
    #                 self.client_sent(msg, good_pack_number)
    #
    #             print("return reached")
    #             return
    #         except:
    #             time.sleep(0.5)
    #             print("waiting....")
    #
    #     print("bad connection")
    #     self.connection_fail += 1
    #     print(f"connection fail {self.connection_fail}")
    #     self.client_sent(msg, good_pack_number)

    def close_socket(self):
        self.client_socket.close()


# this for testing
if __name__ == '__main__':
    pack_size = 3000
    total_time_start = time.time()
    # ask user for pocket lost rate
    while True:
        pocket_lost = input("Please enter pocket_lost number between 0-99:")
        try:
            if 0 < int(pocket_lost) < 99:
                break
        except:
            print(f"{pocket_lost} is not a number between 0-99")
    # ask user for window size for go back n
    window_size = input("Please enter window size:")
    # find total package len of the txt file
    file = open("COSC635_P2_DataSent.txt", "r", encoding="utf8")
    total_pack = int(math.ceil(sys.getsizeof(file.read()) / pack_size))
    i = 1
    all_msg = []
    # making all the data package along with part number and total pack number
    with open("COSC635_P2_DataSent.txt", "r", encoding="utf8") as in_file:
        bytes = in_file.read(pack_size)  # read 5000 bytes
        while bytes:
            # print({"part": i, "total_pack": total_pack})
            msg_pickle = pickle.dumps({"part": i, "total_pack": total_pack, "msg": bytes})
            # client_1.client_sent(msg_pickle, f"part: {i}")
            # total_pack_lost += client_1.connection_fail
            bytes = in_file.read(pack_size)  # read another 5000 bytes
            all_msg.append(msg_pickle)
            i += 1
    # initialize the connection
    # client_1 = ClientServer(pocket_lost, all_msg, window_size, '127.0.0.1', 5010)
    client_1 = ClientServer(pocket_lost, all_msg, window_size, '192.168.10.166', 5010)
    client_1.client_sent_group_pack()
    client_1.close_socket()

    # client_1.close_socket()
    total_time_end = time.time()
    print("Summery:")
    print(f"Total package: {total_pack}")
    print(f"Package Lost rate: {pocket_lost}%")
    print(f"The pack was lost: {client_1.connection_fail - 1} times .")
    print(f"Each package size: {pack_size} bytes")
    print(f"Total time used: {total_time_end-total_time_start} seconds")



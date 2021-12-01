import socket
import pickle


class Receiver:

    def __init__(self, addr, port, store_location):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((addr, port))
        self.total_msg = ""
        self.package_number = 1
        self.store_location = store_location

    def start_listening(self):
        stop_listen = False
        while not stop_listen:
            data, addr = self.sock.recvfrom(4096)
            pack_data = pickle.loads(data)
            print(pack_data["part"], ' out the ', pack_data["total_pack"], " received.")
            if int(pack_data["part"]) == self.package_number:
                self.total_msg += pack_data['msg']
                message = pickle.dumps(f'part: {pack_data["part"]}')
                self.sock.sendto(message, addr)
                self.package_number += 1
            else:
                message = pickle.dumps(f"out of order should sent part: {self.package_number}")
                print(f"Missing part: {self.package_number}")
                self.sock.sendto(message, addr)

            if pack_data['part'] == pack_data['total_pack'] and self.package_number == int(pack_data['total_pack']) + 1:
                stop_listen = True
                text_file = open(self.store_location + r'/COSC635_P2_DataReceived.txt', 'w')
                text_file.write(self.total_msg)
                text_file.close()
                self.sock.close()


if __name__ == '__main__':
    receiver_1 = Receiver("192.168.10.166", 5010, r"C:/Users/wangp.BTC/PycharmProjects/COSC635Project_2/GUI")
    receiver_1.start_listening()



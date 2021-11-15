import socket
import pickle


class Receiver:

    def __init__(self, addr, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((addr, port))
        self.total_msg = ""

    def start_listening(self):
        stop_listen = False
        while not stop_listen:
            data, addr = self.sock.recvfrom(4096)
            pack_data = pickle.loads(data)
            print(pack_data["part"], pack_data["total_pack"])
            self.total_msg += pack_data['msg']
            message = f'part: {pack_data["part"]}'.encode('UTF-8')
            self.sock.sendto(message, addr)
            if pack_data['part'] == pack_data['total_pack']:
                stop_listen = True
                text_file = open('COSC635_P2_DataReceived.txt', 'w')
                text_file.write(self.total_msg)
                text_file.close()


if __name__ == '__main__':
    receiver_1 = Receiver("127.0.0.1", 5005)
    receiver_1.start_listening()



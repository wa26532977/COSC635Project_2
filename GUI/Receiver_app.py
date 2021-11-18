from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QDialog
import sys
import socket
import os
import pickle


class Receiver(QDialog):

    def __init__(self):
        super(Receiver, self).__init__()
        uic.loadUi("Receiver.ui", self)
        self.lineEdit_2.setText(str(socket.gethostbyname(socket.gethostname())))
        self.p_path = os.path.dirname(sys.argv[0])
        self.lineEdit_3.setText(str(self.p_path))
        self.toolButton.clicked.connect(self.open_template)
        self.pushButton.clicked.connect(self.connect_pressed)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(0.1)
        self.checkThreadTimer = QtCore.QTimer(self)
        self.total_msg = ""
        self.package_number = 1

    def connect_pressed(self):
        # make sure port number is entered
        if self.lineEdit.text() == "":
            msgbox = QtWidgets.QMessageBox(self)
            msgbox.setText("Port Number is required!")
            msgbox.exec()
            return
        self.sock.bind((self.lineEdit_2.text(), int(self.lineEdit.text())))
        print("Start Listening...")
        self.checkThreadTimer.timeout.connect(self.start_listening)
        self.checkThreadTimer.start(50)

    def start_listening(self):
        try:
            data, addr = self.sock.recvfrom(4096)
            pack_data = pickle.loads(data)
            # self.listWidget.addItem(pack_data["part"], ' out the ', pack_data["total_pack"], " received.")
            print(pack_data["part"], ' out the ', pack_data["total_pack"], " received.")
            if int(pack_data["part"]) == self.package_number:
                self.listWidget.addItem("received" + str(self.package_number))
                self.total_msg += pack_data['msg']
                message = pickle.dumps(f'part: {pack_data["part"]}')
                self.sock.sendto(message, addr)
                self.package_number += 1
            else:
                self.listWidget.addItem("Missing part" + str(self.package_number))
                message = pickle.dumps(f"out of order should sent part: {self.package_number}")
                print("Missing part" + str(self.package_number))
                self.sock.sendto(message, addr)

            if pack_data['part'] == pack_data['total_pack'] and self.package_number == int(pack_data['total_pack']) + 1:
                self.checkThreadTimer.stop()
                # text_file = open(self.p_path + r'/COSC635_P2_DataReceived.txt', 'w')
                # text_file.write(self.total_msg)
                # text_file.close()
                self.received_finish()
                self.client_socket.close()

        except:
            print("Waiting")

    def received_finish(self):
        text_file = open(self.p_path + r'/COSC635_P2_DataReceived.txt', 'w')
        text_file.write(self.total_msg)
        text_file.close()
        print("finished")
        self.listWidget.addItem("Finish receiving file!")

    def open_template(self):
        os.startfile(self.p_path)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qt_app = Receiver()
    qt_app.show()
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys.excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app.exec_()


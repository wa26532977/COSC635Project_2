from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog
import sys
import os
import pickle
import math
import time
import SenderGBN


class Sender(QDialog):

    def __init__(self):
        super(Sender, self).__init__()
        uic.loadUi("Sender.ui", self)
        self.pushButton.clicked.connect(self.sent_pressed)
        self.lineEdit_2.setText("192.168.10.166")
        self.lineEdit.setText("5010")
        self.pack_size = 0
        self.pocket_lost = 0
        self.window_size = 0
        self.lineEdit_3.setText(os.path.dirname(sys.argv[0])+r'/COSC635_P2_DataSent.txt')

    def sent_pressed(self):
        self.pack_size = int(self.lineEdit_4.text())
        self.pocket_lost = int(self.lineEdit_5.text())
        if self.radioButton.isChecked():
            print("GBN sent")
            self.window_size = 4
        else:
            print("SAW sent")
            self.window_size = 1

        file = open(self.lineEdit_3.text(), 'r', encoding='utf8')
        total_pack = int(math.ceil(sys.getsizeof(file.read()) / self.pack_size))
        # making all the data package along with part number and total pack number
        i = 1
        all_msg = []
        with open(self.lineEdit_3.text(), 'r', encoding='utf8') as in_file:
            payload = in_file.read(self.pack_size)
            while payload:
                msg_pickle = pickle.dumps({"part": i, "total_pack": total_pack, "msg": payload})
                payload = in_file.read(self.pack_size)
                all_msg.append(msg_pickle)
                i += 1
        print(all_msg)
        start_time = time.time()
        client_1 = SenderGBN.ClientServer(
            self.pocket_lost, all_msg, self.window_size, self.lineEdit_2.text(), int(self.lineEdit.text()))
        client_1.client_sent_group_pack()
        client_1.close_socket()
        msgbox = QtWidgets.QMessageBox(self)
        msgbox.setWindowTitle("Summary")
        msgbox.setText(f"File transfer completed:"
                       f"Total time used: {round(time.time() - start_time, 4)} seconds \n"
                       f"Total package: {total_pack} \n"
                       f"The pack was lost: {client_1.connection_fail - 1} times. \n"
                       f"Package Lost rate: {self.pocket_lost}%\n"
                       f"Each package size: {self.pack_size} bytes")
        msgbox.exec()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    qt_app = Sender()
    qt_app.show()
    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys.excepthook(exctype, value, traceback)
        sys.exit(1)

    sys.excepthook = exception_hook

    app.exec_()

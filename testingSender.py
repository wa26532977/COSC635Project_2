import time
import sys
import math
import socket
import pickle

d = {1: "hey", 2: "there"}
msg = pickle.dumps(d)
print(msg)

# arr1 = ['This is good', 'TTTTTTTTTT', 'AAAAAAAAAA']
# msg = np.char.encode(arr1, encoding='utf8', errors='strict')
#
# print(msg)
# start = time.time()
# time.sleep(1)
# end = time.time()
# print(end-start)

# file = open("DataSent.txt", "r", encoding="utf8")
# total_file_size = sys.getsizeof(file.read())
# total_pack = total_file_size / 300
# print(total_pack)
# print(int(math.ceil(total_pack)))
#
# i = 0
# with open("DataSent.txt", "r", encoding="utf8") as in_file:
#     bytes = in_file.read(300)  # read 5000 bytes
#     while bytes:
#         # print(bytes)
#         # print(f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~Part: {i}~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#         msg = bytes.encode('UTF-8')
#         bytes = in_file.read(300)  # read another 5000 bytes
#         i += 1
# print(i)

# with open("DataSent.txt", "r", encoding="utf8") as in_file:
#     bytes = in_file.read(98)  # read 5000 bytes
#     print(bytes)
#     print(sys.getsizeof(bytes))

#
# my_text_binary = " ".join(format(ch, "b") for ch in bytearray(my_text_string))
# print(my_text_binary)
# file = open("DataSent.txt", "r", encoding="utf8")
# total_file_size = sys.getsizeof(file.read())

# msg = 'good'
#
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(msg, ("127.0.0.1", 5006))
data, addr = s.recvfrom(500)
print(str(data))




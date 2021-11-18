import time
import sys
import math
import socket
import pickle

'''
d = {1: "hey", 2: "there"}
msg = pickle.dumps(d)
print(msg)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(0.5)

while True:
    print("trying....")
    s.sendto(msg, ('73.244.13.41', 5005))
    data, addr = s.recvfrom(5000)
    print(str(data))
'''

print(socket.gethostbyname(socket.gethostname()))




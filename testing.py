import numpy as np

arr1 = ['This is good', 'TTTTTTTTTT', 'AAAAAAAAAA']
msg = np.char.encode(arr1, encoding='utf8', errors='strict')

print(msg)
import os
import time

ret = os.fork()
if ret == 0:
	print('-----1-----')
else:
	print('-----2-----')

ret = os.fork()
if ret == 0:
	print('-----11-----')
else:
	print('-----22-----')

import os
import time

def main():
    ret = os.fork()  #win上python的os库没有fork，要在linux云心
    if ret == 0:
        while True:
            print('-----1----')
            time.sleep(1)
    else:
        while True:
            print('------2-----')
            time.sleep(1)

main()
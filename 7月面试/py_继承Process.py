#! /usr/bin/env python
import time
from multiprocessing import Process,Manager

class MyProcess(Process):
    def run(self):
        while True:
            print(self.name)
            time.sleep(1)




def main():
    print("In main...")
    m1 = MyProcess()
    m1.start()
    print("main end...")


if __name__ == "__main__":
    main()



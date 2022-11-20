#! /usr/bin/python
from time import sleep

def work1():
    while True:
        print('--------1-----')
        yield None

def work2():
    while True:
        print('---------2-----')
        yield None

def main():
    w1 = work1()
    w2 = work2()
    while True:
        next(w1)
        sleep(1)
        next(w2)
        sleep(1)

main()
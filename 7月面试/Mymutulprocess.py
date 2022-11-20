#! /usr/bin/env python

import multiprocessing

def work1(count):
    for i in range(count):
        sleep(1)

multiprocessing.Process(target=work1,args=(3))
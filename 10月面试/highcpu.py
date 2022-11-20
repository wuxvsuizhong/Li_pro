import multiprocessing


class MyProcess(multiprocessing.Process):
    def __init__(self):
        super(MyProcess, self).__init__()

    def run(self):
        while True:
            pass


if __name__ == '__main__':
    mlist = []
    for i in range(multiprocessing.cpu_count()):
        mlist.append(MyProcess())

    for each in mlist:
        each.start()

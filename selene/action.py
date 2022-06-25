import threading


class Countdown:
    def __init__(self, name, duration):
        self.s = threading.Timer
        self.p = threading.Timer
        self.duration = duration
        self.tick = 1
        self.name = name
        self.state = False

    def __progress(self):
        self.p = threading.Timer(self.tick, self.__progress)
        self.p.start()
        print("Tick for key {}\n".format(self.name))

    def __finish(self):
        self.state = False
        print("Finished!\n")

    def start(self):
        self.s = threading.Timer(self.duration, self.__finish)
        self.s.start()
        self.__progress()
        self.state = True

    def cancel(self):
        self.state = False
        self.p.cancel()
        self.s.cancel()

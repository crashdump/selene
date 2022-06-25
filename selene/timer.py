import threading


class Timer:
    def __init__(self, duration):
        self.s = threading.Timer
        self.duration = duration
        self.countdown = duration
        self.state = False
        self.callback_tick_method = None
        self.callback_tick_args = None
        self.callback_end_method = None
        self.callback_end_args = None

    def __tick(self):
        if self.state:
            tick = threading.Timer(1, self.__tick)  # tick is 1 second
            tick.start()
            self.countdown = self.countdown - 1
            if self.callback_tick_method is not None:
                print("Tick calling back {} with args {}".format(self.callback_tick_method, self.callback_tick_args))
                self.callback_tick_method(*self.callback_tick_args)
            print("Time tick: {}.".format(self.countdown))

    def __finish(self):
        if self.callback_end_method is not None:
            print("tick calling back {} with args {}".format(self.callback_end_method, self.callback_end_args))
            self.callback_end_method(*self.callback_end_args)
        self.state = False
        print("Timer finished!")

    def start(self):
        self.s = threading.Timer(self.duration, self.__finish)
        self.s.start()
        self.state = True
        self.__tick()

    def cancel(self):
        self.state = False
        self.s.cancel()

    def set_tick_callback(self, method, args=()):
        self.callback_tick_method = method
        self.callback_tick_args = args

    def set_end_callback(self, method, args=()):
        self.callback_end_method = method
        self.callback_tick_args = args

    def get_timer(self):
        return self.s.name

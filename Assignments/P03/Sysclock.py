class SysClock:
    def __init__(self):
        self.clock = 0

    def increment(self):
        self.clock += 1

    def getClock(self):
        return self.clock
    def reset(self):
        self.clock =0
    
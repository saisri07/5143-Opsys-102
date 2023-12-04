class PCB:
    def __init__(self, pid, bursts, at, priority):
        self.pid = pid
        self.priority = priority
        self.arrivalTime = at
        self.bursts = bursts
        self.currBurstIndex = 0
        self.readyQueueTime = 0
        self.waitQueueTime = 0
        self.starvingTime = 0
        
        self.TAT = 0

    
    
    def decrementCpuBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def decrementIoBurst(self):
        self.bursts[self.currBurstIndex] -= 1

    def incrementBurstIndex(self):
        self.currBurstIndex += 1

    def getCurrentBurstTime(self):
        return self.bursts[self.currBurstIndex]

    def incrementReadyQueueTime(self):
        self.readyQueueTime += 1

    def incrementWaitQueueTime(self):
        self.waitQueueTime += 1
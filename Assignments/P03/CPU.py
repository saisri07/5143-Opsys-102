class CPU:
    def __init__(self):
        self.busy = False
        self.runningPCB = None
        self.TotalExecutionTime = 0

    def incrementExecutionTime(self):
        self.TotalExecutionTime += 1

    def decrementCurrentProcess(self):
        self.runningPCB.decrementCpuBurst()

    def loadProcess(self, pcb):
        self.runningPCB = pcb
        self.busy = True

    def isBusy(self):
        return self.busy

    def KickOff(self):
        if self.runningPCB.getCurrentBurstTime() == 0:
            item = self.runningPCB
            self.busy = False
            self.runningPCB = None
            return item
        
    def clearProcess(self):
        self.runningPCB = None
        self.busy = False
class IODevice:
    def __init__(self) -> None:
        self.busy = False
        self.servingPCB = None
        self.TotalExecutionTime = 0
    
    def incrementExecutionTime(self):
        self.TotalExecutionTime += 1

    def decrementCurrentProcess(self):
        self.servingPCB.decrementIoBurst()
    
    def loadProcess(self, pcb):
        self.servingPCB = pcb
        self.busy = True
    
    def KickOff(self):
        if self.servingPCB.getCurrentBurstTime() == 0:
            item = self.servingPCB
            self.busy = False
            self.servingPCB = None
            return item
        
    def isBusy(self):
        return self.busy
    def clearProcess(self):
        self.runningPCB = None
        self.busy = False
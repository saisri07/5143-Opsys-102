class Queue:
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ",".join([str(pcb.pid) for pcb in self.queue])

    def addPCB(self, pcb):
        self.queue.append(pcb)

    def removePCB(self):
        item = self.queue[0]
        del self.queue[0]
        return item

    def incrememnt(self, what='waittime'):
        """ Iterate over the self.queue and decrement or call whatever
            method for each of the pcb's in this queue
        """
        if what == 'waittime':
            for pcb in self.queue:
                pcb.incrementWaitQueueTime()
        elif what == 'runtime':
            for pcb in self.queue:
                pcb.incrementReadyQueueTime()
    
    def getPCBIndex(self, pcb):
        return self.queue.index(pcb)
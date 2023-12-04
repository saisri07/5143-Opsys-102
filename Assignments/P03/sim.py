from rich.console import Console
from rich.table import Table
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
import ast
from Queue import Queue
from Sysclock import SysClock
from CPU import CPU
from IODevice import IODevice
from PCB import PCB

class Simulator:
    def __init__(self, datfile, cpuCount=1, IOCount=1, timeslice=None, speed=None, show=None):
        self.datfile = datfile
        self.timeslice = timeslice if timeslice is not None else 1
        self.speed = speed
        self.new = Queue()
        self.wait = Queue()
        self.ready = Queue()
        self.terminated = Queue()
        self.cpuCount = cpuCount
        self.IOCount = IOCount
        self.running = [CPU() for _ in range(cpuCount)]
        self.IOs = [IODevice() for _ in range(IOCount)]
        self.systemClock = SysClock()
        self.readData()
        self.show = show
        self.console = Console()

    def moveFromNewToReady(self):
        while len(self.new.queue) > 0:
            self.ready.addPCB(self.new.removePCB())

    def ouputWrapper(self):
        pass

    def getRow(self, queue):
        items = [f"[{pcb.pid}, {pcb.priority}] " for pcb in queue]
        return ", ".join(items)

    def printQueuesData(self, message=None):
        table = Table(title="Queues Data")
        table.add_column("Queue", style="cyan", justify="center")
        table.add_column("Processes", style="magenta", justify="center")

        table.add_row("New", self.getRow(list(self.new.queue)))
        table.add_row("Ready", self.getRow(list(self.ready.queue)))
        table.add_row("Running", self.getRow([cpu.runningPCB for cpu in self.running if cpu.runningPCB]))
        table.add_row("Waiting", self.getRow(list(self.wait.queue)))
        table.add_row("IO", self.getRow([io.servingPCB for io in self.IOs if io.servingPCB]))
        table.add_row("Exit", self.getRow(list(self.terminated.queue)))

        self.console.clear()
        self.console.print(table)

        if message:
            self.console.print(message)

        if self.speed is not None:
            time.sleep(float(self.speed))
    def saveData(self, data, filename):
        with open(filename, 'w') as f:
            for line in data:
                f.write(str(line) + '\n')

    def runAllAlgorithms(self):
        algorithms = ['FCFS', 'PB', 'RR']
        data_collection = []

        for algorithm in algorithms:
            self.resetSimulation()
            self.startSimulation(algorithm)
            data_collection.append(self.collectData(algorithm))


        # Save data to a file
        self.saveData(data_collection, 'plot.dat')

    def collectData(self,algorithm):
        # if(algorithm == 'PB'):

        #     print([cpu.TotalExecutionTime for cpu in self.running])
        #     print(self.systemClock.getClock())
        #     sys.exit(1)
        cpu_utilization = sum([cpu.TotalExecutionTime for cpu in self.running]) * 100 / (self.systemClock.getClock() * len(self.running))
        io_utilization = sum([io.TotalExecutionTime for io in self.IOs]) * 100 / (self.systemClock.getClock() * len(self.IOs))
        ave_turnaround_time = sum([p.TAT for p in self.terminated.queue]) / len(self.terminated.queue)
        ave_ready_wait_time = sum([p.readyQueueTime for p in self.terminated.queue]) / len(self.terminated.queue)
        ave_io_wait_time = sum([p.waitQueueTime for p in self.terminated.queue]) / len(self.terminated.queue)

        data = [
            f"Algorithm: {algorithm}",
            f"CPU Utilization: {cpu_utilization}%",
            f"IO Utilization: {io_utilization}%",
            f"Average Turnaround Time: {ave_turnaround_time} s",
            f"Average Ready Wait Time: {ave_ready_wait_time} s",
            f"Average I/O Wait Time: {ave_io_wait_time} s"
        ]

        return data
    
    def plotIndividualGraphs(self):
        # Extract data for plotting
        cpu_utilization = sum([cpu.TotalExecutionTime for cpu in self.running]) * 100 / (self.systemClock.getClock() * len(self.running))
        io_utilization = sum([io.TotalExecutionTime for io in self.IOs]) * 100 / (self.systemClock.getClock() * len(self.IOs))
        ave_turnaround_time = sum([p.TAT for p in self.terminated.queue]) / len(self.terminated.queue)
        ave_ready_wait_time = sum([p.readyQueueTime for p in self.terminated.queue]) / len(self.terminated.queue)
        ave_io_wait_time = sum([p.waitQueueTime for p in self.terminated.queue]) / len(self.terminated.queue)

        # Bar graph for CPU Utilization, IO Utilization, Average Turnaround Time, Average Ready Wait Time, Average I/O Wait Time
        categories = ['CPU Utilization', 'IO Utilization', 'Average Turnaround Time', 'Average Ready Wait Time', 'Average I/O Wait Time']
        values = [cpu_utilization, io_utilization, ave_turnaround_time, ave_ready_wait_time, ave_io_wait_time]
        units = ['%', '%', 's', 's', 's']

        fig, ax = plt.subplots()
        bars = ax.bar(categories, values, color=['blue', 'orange', 'green', 'red', 'purple'])

        # Add values with units on top of each bar
        for bar, value, unit in zip(bars, values, units):
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, f"{round(value, 2)} {unit}", ha='center', va='bottom', color='black', fontweight='bold')

        # Customize the plot
        plt.xlabel("Metrics")
        plt.ylabel("Values")
        plt.title("Performance Metrics")

        # Show the plot
        plt.show("dataFigure.png")





    
    def plotGraphs(self):
    # Read data from the plot.dat file
        with open('plot.dat', 'r') as file:
            data = [line.strip().split(', ') for line in file]

        # Extract data for plotting
        algorithms = [entry[0].split(': ')[1] for entry in data]
        
        cpu_utilization = [round(float(entry[1].split(': ')[1][:-1].split('%')[0]), 2) for entry in data]
        io_utilization = [round(float(entry[2].split(': ')[1][:-1].split('%')[0]), 2) for entry in data]
        turnaround_time = [round(float(entry[3].split(': ')[1][:-2]), 2) for entry in data]
        ready_wait_time = [round(float(entry[4].split(': ')[1][:-2]), 2) for entry in data]
        io_wait_time = [round(float(entry[5].split(': ')[1][:-2].split()[0]), 2) for entry in data]

        # Plotting bar graphs
        fig, axs = plt.subplots(2, 3, figsize=(15, 8))
        axs[1, 2].axis('off')

        axs[0, 0].bar(algorithms, cpu_utilization, color='blue')
        axs[0, 0].set_title('CPU Utilization')
        for i, v in enumerate(cpu_utilization):
            axs[0, 0].text(i, v + 1, f"{v}%", color='blue', ha='center', va='bottom')

        axs[0, 1].bar(algorithms, io_utilization, color='green')
        axs[0, 1].set_title('IO Utilization')
        for i, v in enumerate(io_utilization):
            axs[0, 1].text(i, v + 1, f"{v}%", color='green', ha='center', va='bottom')

        axs[0, 2].bar(algorithms, turnaround_time, color='red')
        axs[0, 2].set_title('Average Turnaround Time')
        for i, v in enumerate(turnaround_time):
            axs[0, 2].text(i, v + 1, f"{v} s", color='red', ha='center', va='bottom')

        axs[1, 0].bar(algorithms, ready_wait_time, color='purple')
        axs[1, 0].set_title('Average Ready Wait Time')
        for i, v in enumerate(ready_wait_time):
            axs[1, 0].text(i, v + 1, f"{v} s", color='purple', ha='center', va='bottom')

        axs[1, 1].bar(algorithms, io_wait_time, color='orange')
        axs[1, 1].set_title('Average I/O Wait Time')
        for i, v in enumerate(io_wait_time):
            axs[1, 1].text(i, v + 1, f"{v} s", color='orange', ha='center', va='bottom')

        # Adjust layout for better visualization
        plt.tight_layout()

        # Show the plot
        plt.show()










    def FCFS(self):
        """ 
        First Come First Serve:
        Queues processes in the order that they arrive in the ready queue.
        """
        while len(self.new.queue) > 0 or len(self.ready.queue) > 0 or len(self.wait.queue) > 0 or any([cpu.runningPCB for cpu in self.running]) or any([io.servingPCB for io in self.IOs]):
            #self.printQueuesData()           
            self.moveFromNewToReady()
            #self.printQueuesData()
            for cpu in self.running:
                if cpu.isBusy():
                    cpu.incrementExecutionTime()
                    cpu.decrementCurrentProcess()
                    kickedOffProcess = cpu.KickOff()
                    if kickedOffProcess:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex != len(kickedOffProcess.bursts):
                            self.wait.addPCB(kickedOffProcess)
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} entered Waiting queue")
                        else:
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.TAT = self.systemClock.getClock() - kickedOffProcess.arrivalTime
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} terminated.\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT}\nRWT = {kickedOffProcess.readyQueueTime}\nIWT = {kickedOffProcess.waitQueueTime}")
            
            if len(self.ready.queue) > 0: 
                for cpu in self.running:
                    if not cpu.isBusy():
                        cpu.loadProcess(self.ready.removePCB())
                        self.printQueuesData(f"At t:{self.systemClock.getClock()} job {cpu.runningPCB.pid} obtained cpu:{self.running.index(cpu)}")
                    if len(self.ready.queue) <= 0:
                        break
                        
            if len(self.wait.queue) > 0:
                for io in self.IOs:
                    if not io.isBusy():
                        io.loadProcess(self.wait.removePCB())
                        self.printQueuesData(f"At t:{self.systemClock.getClock()} job {io.servingPCB.pid} obtained device:{self.IOs.index(io)}")
                    if len(self.wait.queue) <= 0:
                        break

            for io in self.IOs:
                if io.isBusy():
                    io.incrementExecutionTime()
                    io.decrementCurrentProcess()
                    kickedOffProcess = io.KickOff()
                    if kickedOffProcess:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex != len(kickedOffProcess.bursts):
                            self.ready.addPCB(kickedOffProcess)
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} entered Ready queue")
                        else:
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.TAT = self.systemClock.getClock() - kickedOffProcess.arrivalTime
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} terminated.\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT}\nRWT = {kickedOffProcess.readyQueueTime}\nIWT = {kickedOffProcess.waitQueueTime}")
                            
            self.systemClock.increment()
            self.ready.incrememnt(what='runtime')
            self.wait.incrememnt(what='waittime')
            self.readData()

    def PB(self):
        aging_threshold = 20  
        while len(self.ready.queue) > 0 or len(self.wait.queue) > 0 or len(self.new.queue) > 0 or any([cpu.runningPCB for cpu in self.running]) or any([io.servingPCB for io in self.IOs]):
            #self.printQueuesData()
            self.moveFromNewToReady()
            #self.printQueuesData()

            
            for process in self.ready.queue:
                process.starvingTime += 1
                if process.starvingTime >= aging_threshold:
                    process.starvingTime = 0
                    current_priority = int(process.priority[1:])
                    if current_priority > 1:
                        new_priority = current_priority - 1
                        process.priority = f"P{new_priority}"

            for cpu in self.running:
                if cpu.isBusy():
                    cpu.incrementExecutionTime()
                    cpu.decrementCurrentProcess()
                    

                    kickedOffProcess = cpu.KickOff()
                    if not kickedOffProcess :
                        currentPriority = int(cpu.runningPCB.priority[1:])
                        if len(self.ready.queue) > 0:
                            maxPriority = int(self.ready.queue[0].priority[1:])
                            pi = 0

                            for i, process in enumerate(self.ready.queue):
                                newPriority = int(process.priority[1:])
                                if maxPriority < newPriority:
                                    pi = i
                                    maxPriority = newPriority

                            if maxPriority < currentPriority:
                                self.ready.addPCB(cpu.runningPCB)
                                self.printQueuesData(f"At t:{self.systemClock.getClock()} job {cpu.runningPCB.pid} preempted, moved to Ready queue")
                                cpu.clearProcess()
                                cpu.loadProcess(self.ready.queue.pop(pi))
                    else:
                        kickedOffProcess.incrementBurstIndex()  
                        if kickedOffProcess.currBurstIndex != len(kickedOffProcess.bursts):
                            self.wait.addPCB(kickedOffProcess)
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} entered Waiting queue")
                        else:
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.TAT = self.systemClock.getClock() - kickedOffProcess.arrivalTime
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} terminated.\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT}\nRWT = {kickedOffProcess.readyQueueTime}\nIWT = {kickedOffProcess.waitQueueTime}")

            if len(self.ready.queue) > 0:
                for cpu in self.running:
                    if not cpu.isBusy():
                        pi = 0
                        maxPriority = int(self.ready.queue[0].priority[1:])
                        for i, process in enumerate(self.ready.queue):
                            newPriority = int(process.priority[1:])
                            if maxPriority > newPriority:
                                pi = i
                                maxPriority = newPriority
                        cpu.loadProcess(self.ready.queue.pop(pi))
                        self.printQueuesData(f"At t:{self.systemClock.getClock()} job {cpu.runningPCB.pid} obtained cpu:{self.running.index(cpu)}")
                    if len(self.ready.queue) <= 0:
                        break

            if len(self.wait.queue) > 0:
                for io in self.IOs:
                    if not io.isBusy():
                        io.loadProcess(self.wait.removePCB())
                        self.printQueuesData(f"At t:{self.systemClock.getClock()} job {io.servingPCB.pid} obtained device:{self.IOs.index(io)}")
                    if len(self.wait.queue) <= 0:
                        break

            for io in self.IOs:
                if io.isBusy():
                    io.incrementExecutionTime()
                    io.decrementCurrentProcess()
                    kickedOffProcess = io.KickOff()
                    if kickedOffProcess:
                        kickedOffProcess.incrementBurstIndex()
                        
                        if kickedOffProcess.currBurstIndex != len(kickedOffProcess.bursts):
                            self.ready.addPCB(kickedOffProcess)
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} entered Ready queue")
                        else:
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.TAT = self.systemClock.getClock() - kickedOffProcess.arrivalTime
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} terminated.\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT}\nRWT = {kickedOffProcess.readyQueueTime}\nIWT = {kickedOffProcess.waitQueueTime}")

            self.systemClock.increment()
            self.ready.incrememnt(what='runtime')
            self.wait.incrememnt(what='waittime')
            self.readData()



    def RR(self):
        """ Round Robin
        """
        while len(self.ready.queue) > 0 or len(self.wait.queue) > 0 or len(self.new.queue) > 0 or any([cpu.runningPCB for cpu in self.running]) or any([io.servingPCB for io in self.IOs]):
            # self.printQueuesData()
            self.moveFromNewToReady()
            # self.printQueuesData()
            
            for cpu in self.running:
                if cpu.isBusy():
                    cpu.incrementExecutionTime()
                    cpu.decrementCurrentProcess()

                    kickedOffProcess = cpu.KickOff()
                    if not kickedOffProcess:
                        if cpu.TotalExecutionTime % self.timeslice == 0:
                            self.ready.addPCB(cpu.runningPCB)
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {cpu.runningPCB.pid} preempted, moved to Ready queue")
                            cpu.clearProcess()
                    else:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex != len(kickedOffProcess.bursts):
                            self.wait.addPCB(kickedOffProcess)
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} entered Waiting queue")
                        else:
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.TAT = self.systemClock.getClock() - kickedOffProcess.arrivalTime
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} terminated.\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT}\nRWT = {kickedOffProcess.readyQueueTime}\nIWT = {kickedOffProcess.waitQueueTime}")

            if len(self.ready.queue) > 0: 
                for cpu in self.running:
                    if not cpu.isBusy():
                        cpu.loadProcess(self.ready.removePCB())
                        self.printQueuesData(f"At t:{self.systemClock.getClock()} job {cpu.runningPCB.pid} obtained cpu:{self.running.index(cpu)}")
                    if len(self.ready.queue) <= 0:
                        break

            if len(self.wait.queue) > 0:
                for io in self.IOs:
                    if not io.isBusy():
                        io.loadProcess(self.wait.removePCB())
                        self.printQueuesData(f"At t:{self.systemClock.getClock()} job {io.servingPCB.pid} obtained device:{self.IOs.index(io)}")
                    if len(self.wait.queue) <= 0:
                        break

            for io in self.IOs:
                if io.isBusy():
                    io.incrementExecutionTime()
                    io.decrementCurrentProcess()
                    kickedOffProcess = io.KickOff()
                    if kickedOffProcess:
                        kickedOffProcess.incrementBurstIndex()
                        if kickedOffProcess.currBurstIndex != len(kickedOffProcess.bursts):
                            self.ready.addPCB(kickedOffProcess)
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} entered Ready queue")
                        else:
                            self.terminated.addPCB(kickedOffProcess)
                            kickedOffProcess.TAT = self.systemClock.getClock() - kickedOffProcess.arrivalTime
                            self.printQueuesData(f"At t:{self.systemClock.getClock()} job {kickedOffProcess.pid} terminated.\nST = {kickedOffProcess.arrivalTime} \nTAT = {kickedOffProcess.TAT}\nRWT = {kickedOffProcess.readyQueueTime}\nIWT = {kickedOffProcess.waitQueueTime}")

            self.systemClock.increment()
            self.ready.incrememnt(what='runtime')
            self.wait.incrememnt(what='waittime')
            self.readData()
            
    def readData(self):
        with open(self.datfile) as f:
            data = f.read().split("\n")

        for process in data:
            if len(process) > 0:
                parts = process.split(' ')
                arrival = parts[0]
                pid = parts[1]
                priority = parts[2]
                bursts = parts[3:]
                bursts = list(map(int, bursts))
                if self.systemClock.getClock() == int(arrival):
                    self.new.addPCB(PCB(int(pid), bursts, int(arrival), priority))

    def showStat(self):
        print
        cpuUtilization = sum([cpu.TotalExecutionTime for cpu in self.running]) * 100 / (self.systemClock.getClock() * len(self.running))
        ioUtilization = sum([io.TotalExecutionTime for io in self.IOs]) * 100 / (self.systemClock.getClock() * len(self.IOs))
        aveTurnaroundTime = sum([p.TAT for p in self.terminated.queue]) / len(self.terminated.queue)
        aveWaitTime = sum([p.readyQueueTime for p in self.terminated.queue]) / len(self.terminated.queue)
        aveIOTime = sum([p.waitQueueTime for p in self.terminated.queue]) / len(self.terminated.queue)

        stat_table = Table(title="Statistics", style="green")
        stat_table.add_column("Stat", style="bold")
        stat_table.add_column("Value", style="bold")

        stat_table.add_row("CPU Utilization", f"{cpuUtilization}%")
        stat_table.add_row("IO Utilization", f"{ioUtilization}%")
        stat_table.add_row("Average Turnaround Time",str(aveTurnaroundTime))
        stat_table.add_row("Average Ready Wait Time",str(aveWaitTime))
        stat_table.add_row("Average I/O Wait Time",str(aveIOTime))

        self.console.print(stat_table)

    def resetSimulation(self):
        # Clear queues
        self.new = Queue()
        self.wait = Queue()
        self.ready = Queue()
        self.terminated = Queue()
        self.running = [CPU() for _ in range(self.cpuCount)]
        self.IOs = [IODevice() for _ in range(self.IOCount)]
        # Reset CPUs
        for cpu in self.running:
            cpu.clearProcess()

        # Reset IO devices
        for io in self.IOs:
            io.clearProcess()

        # Reset system clock
        self.systemClock.reset()

        # Read data again
        self.readData()

        # Reset console
        self.console = Console()

    def startSimulation(self, algorithm):
        self.ouputWrapper()
        if algorithm == 'FCFS':
            self.FCFS()
        elif algorithm == 'PB':
            self.PB()
        elif algorithm == 'RR':
            self.RR()
        elif algorithm == 'ALL':
            self.RR()
        else:
            print("Invalid algorithm")
            sys.exit(1)
        self.showStat()
        if(self.show is not None):
            self.plotIndividualGraphs()
        

    # def plotGraphs(self, algorithm):
    #     # ... (previous code)
    #     plt.title(f"Performance Metrics - {algorithm}")  # Set a title including the algorithm name
    #     plt.show()

if __name__ == '__main__':
    try:
        if len(sys.argv) < 4:
            raise Exception("Invalid number of arguments")
        params = {}
        for arg in sys.argv[1:]:
            key, value = arg.split('=')
            params[key] = value
        print(params)
        if params['sched'] == "RR" and 'timeslice' not in params:
            raise Exception("Time Quantum is required for RR")
    except Exception as e:
        print(e)
        print()
        print("Usage: python sim.py sched=RR timeslice=3 cpus=4 ios=6 input=filename.dat")
        print("""Scheduling Algorithm:
                FCFS: First Come First Serve
                PB: Priority Based
                RR: Round Robin""")
        sys.exit(1)
    speed = float(params['speed']) if 'speed' in params and params['speed'] is not None else None
    show = ast.literal_eval(params['show']) if 'show' in params and params['show'] is not None else None

    sim = Simulator(params['input'], int(params['cpus']), int(params['ios']),
                int(params['timeslice']) if params['sched'] == "RR" else None,
                speed,
                show=show)
    if params['sched'] == "ALL":
        sim.runAllAlgorithms()

        print("Data for all algorithms saved in 'plot.dat'.")
        sim.plotGraphs()
    else:
        sim.startSimulation(params['sched'])
    

    
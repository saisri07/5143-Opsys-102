
# Nov 3 2023

## Cpu Scheduling - Simulation

## Group Members
* Sai Teja Sripathi
* Sai Neeraj Chandragiri
* Naveen Kumar Poka

## Overview:
Early computers had CPUs that were mostly idle, which gave rise to the classic and modern computer science problem of CPU scheduling. Initially, loading multiple programs into memory allowed them to execute simultaneously. This still needed to be improved because it was inefficient. This quickly developed into the loading of many programs into memory, which allowed the CPU to work on other processes that were accessible when one process blocked itself (multi-programming). Naturally, this continued to change as our world became more multi-threaded and multi-processor. But we still have to remember to keep the CPU(s) active! 

## Supported algorithms
* First Come First Serve / FCFS
* Round-Robin / RR
* Priority Based

## Built with
* Python
* rich

### Installation Process :
pip install -r requirement.txt

#### After completing all the necessary packages run one of the following commands

python3 sim.py sched=FCFS cpus=5 ios=5  input=small_file.dat  speed=1

python3 sim.py sched=FCFS cpus=1 ios=1  input=small_file.dat  speed=0.5
python3 sim.py sched=FCFS cpus=2 ios=2  input=small_cpu.dat  speed=0.02

python3 sim.py sched=RR  cpus=2 ios=2  input=small_io.dat  speed=0.05 timeslice=10
python3 sim.py sched=RR  cpus=2 ios=5  input=small_io.dat  speed=0.02 timeslice=10

python3 sim.py sched=PB  cpus=3 ios=3  input=small_file.dat  speed=0.5
python3 sim.py sched=PB  cpus=3 ios=3  input=small_highpriorityfile.dat  speed=0.5

python3 sim.py sched=RR cpus=10 ios=10  input=mid_file.dat timeslice=15
python3 sim.py sched=FCFS cpus=20 ios=15  input=big_file.dat 

python3 sim.py sched=ALL cpus=2 ios=2  input=small_cpu.dat
  



#### Required Parameters:

 type   = algorithm type [FCFS or RR or PB]
        
 cpus   = number of CPU (e.g., 5, 2)
        
 ios    = number of IO (e.g., 2, 6)
        
 input  = process contain file (e.g., small.dat)  
        
#### Optional Parameters:

  timeslice = required for RR, default 5
        
  speed     = default 0.01 or accepts any values






















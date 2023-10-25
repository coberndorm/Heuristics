import numpy as np
import auxiliar_functions as af

# Define job class
class Job:
    def __init__(self, mach_req, proc_time, number, rand=0.1):
        self.mach_req = mach_req  # Machines required for the job
        self.proc_time = np.array(proc_time)  # Processing times for the job on each machine
        self.processes = [i + (number-1)*len(mach_req) for i in range(1,len(mach_req)+1)]
        self.free_time_real = 0  # Time when the job becomes available for scheduling (real time)
        self.rand = rand  # Randomness factor
        
        rand_val = np.floor(self.proc_time*np.random.random(size=self.proc_time.size)*rand) # Random values for the job on each machine
        self.proc_time_random = self.proc_time + rand_val  # Randomized processing times for the job on each machine
        self.stage = [False] * len(mach_req)  # Stages of the job completed on machines
        self.counter = 0  # Index to track the current machine for the job
        self.number = number  # Job number
        self.free_time = 0  # Time when the job becomes available for scheduling
        self.job_done = False  # Flag to indicate if the job is completed

    def __lt__(self, other):
        # Comparison method to determine if this job has a shorter processing time
        return self.proc_time[self.counter] < other.proc_time[other.counter]
    
    def __add__(self, other):
        # Add the job's processing time to another object's free time
        return self.proc_time[self.counter] + other.free_time
    
    def __le__(self, other):
        # Comparison method to determine if this job can be scheduled on a machine
        return self.free_time <= other.free_time
    
    def __bool__(self):
        # Boolean representation of a job indicating if it's completed
        return self.job_done
    

# Define machine class
class Machine:
    def __init__(self, number):
        self.free = True  # Flag to indicate if the machine is free
        self.free_time = 0  # Time when the machine becomes available for scheduling
        self.free_time_real = 0  # Time when the machine becomes available for scheduling (real time)
        self.number = number  # Machine number

    def __lt__(self, other):
        # Comparison method to determine if this machine has a shorter free time
        return self.free_time < other.free_time
    
    def __le__(self, other):
        # Comparison method to determine if this machine has an earlier or equal free time
        return self.free_time <= other.free_time

    
def shortest_job(jobs,mach):
    # Set the number of the machine free
    mach_num = mach.number

    # Initialize arrays for available jobs and their processing times
    job_mach_free = []; job_mach_free_real = []

    for job in jobs:
        # Get processing times for jobs that require the current machine
        # Considerar como cambia el algoritmo si se pone mach <= job
        if not job.job_done and job.mach_req[job.counter] == mach_num:
            if job <= mach:
                job_mach_free.append(job)
            if job.free_time_real <= mach.free_time_real:
                job_mach_free_real.append(job)
        
    if job_mach_free_real == []:
        mach.free_time_real += 1

    if job_mach_free == []:
        mach.free_time += 1
        return
        
    
    # Find the job with the shortest processing time
    job_next = min(job_mach_free)
    if job_next.free_time != mach.free_time:
        job_next.free_time = mach.free_time
    
    if job_next.free_time_real != mach.free_time_real:
        job_next.free_time_real = mach.free_time_real
    

    processing_time = job_next.proc_time_random[job_next.counter]
    processing_time_real = job_next.proc_time[job_next.counter]

    # Mark the job as done for this stage
    process_done = job_next.processes[job_next.counter]
    job_next.stage[job_next.counter] = True
    job_next.counter += 1
    if all(job_next.stage):
        job_next.job_done = True

    return job_next, processing_time, processing_time_real, process_done


def order(jobs, machines):
    # Initialize answer list
    # name as follows dict(Task=, Start=, End=, Resource=)
    ans_aleatorio = []

    # Track the order in which jobs pass through each machine
    machine_order = [[] for _ in range(len(machines))]
    process_order = [[] for _ in range(len(machines))]

    while not all(jobs):
        # Find the machine with the earliest free time
        mach = min(machines)

        next_proc = shortest_job(jobs, mach)
        if next_proc != None:
            job_next, processing_time, processing_time_real, process = next_proc[0], next_proc[1], next_proc[2], next_proc[3]
        else:
            continue

        # Add the job's info to the answer list
        ans_aleatorio.append({
            'Task': 'Job ' + str(job_next.number),
            'Start': mach.free_time_real,
            'End': mach.free_time_real + processing_time_real,
            'Resource': 'M. ' + str(mach.number)
        })

        # Update the machine's free time
        job_next.free_time += processing_time
        job_next.free_time_real += processing_time_real
        mach.free_time += processing_time
        mach.free_time_real += processing_time_real
    
        # Track the order in which this job passed through the machine
        machine_order[mach.number - 1].append(job_next.number)
        process_order[mach.number - 1].append(process)
    
    return ans_aleatorio, machine_order, process_order

def aleatorio(jobs, machines, processing_time, machines_required, iterations=500):
    best = 10000000000000
    n = len(jobs); m = len(machines)
    for _ in range(iterations):
        jobs_copy = [Job(job.mach_req, job.proc_time, job.number, job.rand) for job in jobs]
        machines_copy = [Machine(machine.number) for machine in machines]
        _, machine_order, process_order = order(jobs_copy, machines_copy)
        if af.feasible(machine_order, machines_required, n, m) == False:
            continue
        time = af.makespan(machine_order, processing_time, machines_required, n, m)
        if time < best:
            best = time
            best_order = machine_order
            best_process_order = process_order
    return best, best_order, best_process_order

    
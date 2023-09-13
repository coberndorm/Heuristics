# Define job class
class Job:
    def __init__(self, mach_req, proc_time, number):
        self.mach_req = mach_req  # Machines required for the job
        self.proc_time = proc_time  # Processing times for the job on each machine
        self.stage = [False] * len(mach_req)  # Stages of the job completed on machines
        self.counter = 0  # Index to track the current machine for the job
        self.mach_needed = self.mach_req[0]  # Current machine needed for the job
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
        self.number = number  # Machine number

    def __lt__(self, other):
        # Comparison method to determine if this machine has a shorter free time
        return self.free_time < other.free_time
    
    def __le__(self, other):
        # Comparison method to determine if this machine has an earlier or equal free time
        return self.free_time <= other.free_time
    
# Auxiliary function to insert a machine in a sorted array
def insert(lst, machine):
    l = len(lst)
    index = 0
    for i in range(l):
        if lst[i].free_time >= machine.free_time:
            index = i
            break
        index = i
    lst.insert(index+1, machine)
    return lst

# Function to find the shortest job available for a machine
def shortest_job(jobs, mach):
    # Get the number of the machine that is free
    mach_num = mach.number

    # Initialize arrays for available jobs and their processing times
    job_mach_free = []

    for job in jobs:
        # Check if the job is not done, needs the current machine, and can be scheduled
        if not job.job_done and job.mach_req[job.counter] == mach_num and job <= mach:
            job_mach_free.append(job)
        
    if not job_mach_free:
        # No available jobs for this machine at the moment, increment machine's free time
        mach.free_time += 1
        return
    
    # Find the job with the shortest processing time
    job_next = min(job_mach_free)
    
    if job_next.free_time != mach.free_time:
        # Synchronize the job's free time with the machine's free time
        job_next.free_time = mach.free_time
    
    processing_time = job_next.proc_time[job_next.counter]

    # Mark the job as done for this stage
    job_next.stage[job_next.counter] = True
    job_next.counter += 1
    
    if all(job_next.stage):
        # If all stages of the job are completed, mark it as done
        job_next.job_done = True

    return job_next, processing_time

# Main constructive scheduling function
def constructivo(jobs, machines):
    # Initialize answer list
    # Format: dict(Task=, Start=, End=, Resource=)
    ans = []

    # Track the order in which jobs pass through each machine
    machine_order = [[] for _ in range(len(machines))]

    while not all(jobs):
        # Find the machine with the earliest free time
        mach = min(machines)
        
        aux = shortest_job(jobs, mach)
        
        if aux is not None:
            job_next, processing_time = aux[0], aux[1]
        else:
            continue

        # Add the job's info to the answer list
        ans.append({
            'Task': 'Job ' + str(job_next.number),
            'Start': mach.free_time,
            'End': mach.free_time + processing_time,
            'Resource': 'M. ' + str(mach.number)
        })

        # Track the order in which this job passed through the machine
        machine_order[mach.number - 1].append(job_next.number)

        # Update the machine's free time and the job's free time
        job_next.free_time += processing_time
        mach.free_time += processing_time
    
    return ans
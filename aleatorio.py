# Define job class
class Job:
    def __init__(self, mach_req, proc_time, number):
        self.mach_req = mach_req
        self.proc_time = proc_time
        
        self.stage = [False] * len(mach_req)
        self.counter = 0
        self.mach_needed = self.mach_req[0]
        self.number = number
        self.free_time = 0
        self.job_done = False
        
    
    def __lt__(self, other):
        return self.proc_time[self.counter] < other.proc_time[other.counter]
    
    def __add__(self, other):
        return self.proc_time[self.counter] + other.free_time
    
    def __le__(self, other):
        return self.free_time <= other.free_time
    
    def __bool__(self):
        return self.job_done
    

# Define machine class
class Machine:
    def __init__(self, number):
        self.free = True
        self.free_time = 0
        self.number = number

    def __lt__(self, other):
        return self.free_time < other.free_time
    
    def __le__(self, other):
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

def shortest_job(jobs,mach):
    # Set the number of the machine free
    mach_num = mach.number

    # Initialize arrays for available jobs and their processing times
    job_mach_free = []

    for job in jobs:
        # Get processing times for jobs that require the current machine
        # Considerar como cambia el algoritmo si se pone mach <= job
        if not job.job_done and job.mach_req[job.counter] == mach_num and job <= mach:
            job_mach_free.append(job)
        
    if job_mach_free == []:
        mach.free_time += 1
        return
    
    # Find the job with the shortest processing time
    job_next = min(job_mach_free)
    if job_next.free_time != mach.free_time:
        job_next.free_time = mach.free_time
    
    processing_time = job_next.proc_time[job_next.counter]

    # Mark the job as done for this stage
    job_next.stage[job_next.counter] = True
    job_next.counter += 1
    if all(job_next.stage):
        job_next.job_done = True

    return job_next, processing_time


def constructivo(jobs, machines):
    # Initialize answer list
    # name as follows dict(Task=, Start=, End=, Resource=)
    ans = []

    while not all(jobs):
        # Find the machine with the earliest free time
        mach = min(machines)
        mach_num = mach.number

        a = shortest_job(jobs, mach)
        if a != None:
            job_next, processing_time = a[0], a[1]
        else:
            continue

        # Add the job's info to the answer list
        ans.append({
            'Task': 'Job ' + str(job_next.number),
            'Start': mach.free_time,
            'End': mach.free_time + processing_time,
            'Resource': 'M. ' + str(mach.number)
        })

        # Update the machine's free time
        job_next.free_time += processing_time
        mach.free_time += processing_time
    
    return ans

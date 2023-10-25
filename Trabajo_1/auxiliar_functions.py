import numpy as np

def feasible(sol, order, jobs, machines):
    # Initialize arrays to keep track of the next job and machine for each job and machine
    next_machine = np.zeros(jobs, dtype=int)
    next_job = np.zeros(machines, dtype=int)

    # Initialize a flag to control the loop
    stop = False

    # Continue looping until the flag is True
    while not stop:
        # Count the number of machines that have not finished their jobs
        avl_machines = 0
        for m in range(machines):
            if next_job[m] < jobs:
                avl_machines += 1

        # Initialize a count for machines that cannot process the next job
        count = 0

        # Loop through machines
        for m in range(machines):
            if next_job[m] < jobs:
                # Get the next process to be done in the machine
                job = sol[m][next_job[m]]
                # Check if the job has already been done in the previous processes
                j = job - 1
                machine = order[j][next_machine[j]]
                
                # If the machine can process the next job, update counters
                if machine == m+1:
                    next_job[m] += 1
                    next_machine[j] += 1
                else:
                    # Increment the count of machines that cannot process the next job
                    count += 1

        # If the count of machines that cannot process the next job equals
        # the total available machines, stop the loop
        if avl_machines == count:
            stop = True

    # Check if all machines have processed all their jobs to determine feasibility
    for j in range(jobs):
        if next_machine[j] < machines:
            # If a machine has not processed all the jobs, the solution is not feasible
            return False
    
    # If all machines have processed all their jobs, the solution is feasible
    return True


def makespan(sol, timep, order, jobs, machines):
    # Initialize arrays to keep track of the next job, machine, and time for each job and machine
    next_machine = np.zeros(jobs, dtype=int)
    next_job = np.zeros(machines, dtype=int)
    time_machines = np.zeros(machines, dtype=int)
    time_jobs = np.zeros(jobs, dtype=int)

    # Initialize a flag to control the loop
    stop = False

    # Continue looping until the flag is True
    while not stop:
        stop = True

        # Loop through machines
        for m in range(machines):
            if next_job[m] < jobs:
                # Get the next process to be done in the machine
                job = sol[m][next_job[m]]
                j = job - 1
                machine = order[j][next_machine[j]]
                
                # If the machine can process the next job, update time and counters
                if machine == m+1:
                    time_jobs[j] = max(time_jobs[j], time_machines[m]) + timep[j][next_machine[j]]
                    time_machines[m] = time_jobs[j]

                    next_job[m] += 1
                    next_machine[j] += 1
        
        # Check if any job still needs processing by a machine
        for j in range(jobs):
            if next_machine[j] < machines:
                stop = False
                break

    # Return the maximum time taken by any machine as makespan
    return max(time_machines)

def sol_matrix_to_vector(machine_order, machines_required, n ,m):
    processes_num = dict()
    processes_num = {(i+1,machines_required[i][j]): i * m + j +1 for i in range(n) for j in range(m)}
    # vectorizing the solution matrix
    machine_order_vector = [processes_num[(machine_order[j][i],j+1)] for i in range(n) for j in range(m)]
    return machine_order_vector

def sol_vector_to_matrix(machine_order_vector, machines_required, n ,m):
    processes_num = dict()
    processes_num = {i * m + j +1: i+1 for i in range(n) for j in range(m)}

    # Turn the vector back into a matrix
    machine_order_matrix = [[processes_num[machine_order_vector[i * m + j]] for i in range(n)] for j in range(m)]
    return machine_order_matrix
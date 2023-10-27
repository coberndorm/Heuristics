from auxiliar_functions import *
import time
import random
import copy


def interchange(sol, i, j, mach):
    # move the value in position i to the position j in the machine mach
    sol_copy = sol[:mach]
    new_line = sol[mach][0:i] + [sol[mach][j]] + sol[mach][i+1:j] + [sol[mach][i]] + sol[mach][j+1:]
    sol_copy += [new_line] + sol[mach+1:]
    return sol_copy

def insert_forward(sol, i, j, mach):
    # insert the value in position j to the position ji in the machine mach
    sol_copy = sol[:mach]
    new_line = sol[mach][0:i] + [sol[mach][j]] + sol[mach][i:j] + sol[mach][j+1:]
    sol_copy += [new_line] + sol[mach+1:]
    return sol_copy

def insert_backward(sol, i, j, mach):
    # insert the value in position j to the position ji in the machine mach
    sol_copy = sol[:mach]
    new_line = sol[mach][0:i] + sol[mach][i+1:j+1] + [sol[mach][i]] + sol[mach][j+1:]
    sol_copy += [new_line] + sol[mach+1:]
    return sol_copy


def first_improvement(constr, processing_time, machines_required, n, m, method = interchange):

    sol = constr; sol_time = makespan(sol, processing_time, machines_required, n, m)
    stop = False


    while stop == False:
        stop = True
        for mach in range(m):
            for i in range(n):
                for j in range(i+1, n):
                    new_sol = method(sol, i, j, mach)
                    if feasible(new_sol, machines_required, n, m) == False:
                        continue
                    new_sol_time = makespan(new_sol, processing_time, machines_required, n, m)
                    if new_sol_time < sol_time:
                        sol = new_sol; sol_time = new_sol_time
                        stop = False
                        break
                if stop == False:
                    break
            if stop == False:
                    break
    return sol


def best_improvement(constr, processing_time, machines_required, n, m, method = interchange):
    
    move = lambda sol, i, j: sol[0:i] + [sol[j]] + sol[i+1:j] + [sol[i]] + sol[j+1:]

    sol = constr; sol_time = makespan(sol, processing_time, machines_required, n, m)
    stop = False
    sol_best = sol; sol_time_best = sol_time

    while stop == False:
        stop = True
        for mach in range(m):
            for i in range(n):
                for j in range(i+1, n):
                    new_sol = method(sol, i, j, mach)
                    if feasible(new_sol, machines_required, n, m) == False:
                        continue
                    new_sol_time = makespan(new_sol, processing_time, machines_required, n, m)
                    if new_sol_time < sol_time_best:
                        sol_best = new_sol; sol_time_best = new_sol_time
                        stop = False

        if stop == False:
            sol = sol_best; sol_time = sol_time_best
                    
    return sol

def variable_neighborhood_search(constr, processing_time, machines_required, n, m, methods = [interchange, insert_forward, insert_backward], max_time = 60):
    sol = constr; sol_time = makespan(sol, processing_time, machines_required, n, m)
    stop = False
    sol_best = sol; sol_time_best = sol_time
    start_time = time.time()

    while stop == False and time.time() - start_time < max_time:
        stop = True
        counter = 0

        while counter < len(methods) and time.time() - start_time < max_time:
            for mach in range(m):
                for i in range(n):
                    for j in range(i+1, n):
                        method = methods[counter]
                        new_sol = method(sol, i, j, mach)

                        if feasible(new_sol, machines_required, n, m) == False:
                            if counter <= len(methods) - 1:
                                break
                            else:
                                continue
                        
                        new_sol_time = makespan(new_sol, processing_time, machines_required, n, m)

                        if new_sol_time < sol_time_best:
                            counter = 0
                            sol_best = new_sol; sol_time_best = new_sol_time
                            stop = False
            counter += 1
                        
        if stop == False:
            sol = sol_best; sol_time = sol_time_best  
                    
    return sol


def reduced_neighborhood_search(constr, processing_time, machines_required, n, m, neighborhoods = [interchange, insert_forward, insert_backward], times_to_test = 10):
    sol = constr; sol_time = makespan(sol, processing_time, machines_required, n, m)
    stop = False

    while stop == False:
        stop = True
        method = 0
        while method < len(neighborhoods):
            times_tested = 1
            while times_tested <= times_to_test:
                i = np.random.randint(0, n-1); j = np.random.randint(i+1, n); mach = np.random.randint(0, m)
                if i == j:
                    continue
                new_sol = neighborhoods[method](sol, i, j, mach)
                if feasible(new_sol, machines_required, n, m) == False:
                    continue
                new_sol_time = makespan(new_sol, processing_time, machines_required, n, m)
                times_tested += 1
                if new_sol_time < sol_time:
                    method=0
                    sol = new_sol; sol_time = new_sol_time
                    stop = False
                    break
            
            if times_tested >= times_to_test:
                method += 1
                
                    
    return sol


def far_neighborhoods_seach(constr, processing_time, machines_required, n, m, methods = [interchange, insert_forward, insert_backward]):

    sol = constr; sol_time = makespan(sol, processing_time, machines_required, n, m)
    stop = False
    sol_best = sol; sol_time_best = sol_time

    while stop == False:
        stop = True
        for mach in range(m):
            for i in range(n):
                for j in range(i+1, n):
                    new_sol = sol

                    for method in methods:
                        new_sol = method(new_sol, i, j, mach)
                    
                    if feasible(new_sol, machines_required, n, m) == False:
                        continue

                    new_sol_time = makespan(new_sol, processing_time, machines_required, n, m)
                    
                    if new_sol_time < sol_time_best:
                        sol_best = new_sol; sol_time_best = new_sol_time
                        stop = False

        if stop == False:
            sol = sol_best; sol_time = sol_time_best
                    
    return sol



def recocido(sol, processing_time, machines_required, n, m, method = interchange, max_time = 10, max_iter= 100, T0 = 100, alpha = 0.9, T_min = 0.1):
    
    sol_time = makespan(sol, processing_time, machines_required, n, m)
    stop = False

    start_time = time.time()

    while time.time() - start_time < max_time and stop == False:
        stop = True
        T = T0

        while T > T_min:
            for _ in range(max_iter):
                
                i = np.random.randint(0, n-1); j = np.random.randint(i+1, n); mach = np.random.randint(0, m)
                if i == j:
                    continue
                new_sol = method(sol, i, j, mach)

                if feasible(new_sol, machines_required, n, m) == False:
                    continue
                
                new_sol_time = makespan(new_sol, processing_time, machines_required, n, m)

                if new_sol_time < sol_time:
                    stop = False
                    sol = new_sol; sol_time = new_sol_time

                else:
                    r = random.random()
                    if r < np.exp((sol_time - new_sol_time)/T):
                        sol = new_sol; sol_time = new_sol_time
                        stop = False

            T = alpha * T
        
                    
    return sol

def simple_multi_search(multiple_sol, processing_time, machines_required, n, m, method = interchange, noise_selection_prob = 0.01):
    best_sol = multiple_sol[0]; best_sol_time = makespan(best_sol, processing_time, machines_required, n, m)

    for sol in multiple_sol:

        sol_time = makespan(sol, processing_time, machines_required, n, m)
        stop = False
        sol_best = sol; sol_time_best = sol_time

        while stop == False:
            stop = True
            for mach in range(m):
                for i in range(n):
                    for j in range(i+1, n):
                        new_sol = method(sol, i, j, mach)
                        if feasible(new_sol, machines_required, n, m) == False:
                            continue
                        new_sol_time = makespan(new_sol, processing_time, machines_required, n, m)
                        if new_sol_time < sol_time_best:
                            sol_best = new_sol; sol_time_best = new_sol_time
                            stop = False

            if stop == False or random.random() < noise_selection_prob:
                sol = sol_best; sol_time = sol_time_best
        
        if sol_time < best_sol_time:
            best_sol = sol; best_sol_time = sol_time
                    
    return best_sol

def repair_method(destroyed_jobs, sol, machines_required, n, m, max_iter=100):

    while True:

        new_sol = copy.deepcopy(sol)

        # Insert the shuffled values into the target list
        for mach in destroyed_jobs.keys():
            for job in destroyed_jobs[mach]:
                index_to_insert = random.randint(0, len(new_sol[mach-1]))
                new_sol[mach-1].insert(index_to_insert,job)

        if feasible(new_sol, machines_required, n, m):
            return new_sol
        
        if max_iter == 0:
            return None
        
        max_iter -= 1

def LNS(sol, n,m, machines_required, lns_destroy_percentage=0.1):
    processes_num = {i * m + j +1: (i+1,machines_required[i][j])  for i in range(n) for j in range(m)}
    job_size = n*m
    sol_copy = copy.deepcopy(sol)
    num_jobs_to_destroy = int(lns_destroy_percentage * job_size)
    destroyed_indices = random.sample(range(1,job_size+1), num_jobs_to_destroy)

    # Remove the jobs from the solution
    destroyed_jobs = {i:[] for i in range(1,m+1)}
    for index in destroyed_indices:
        job, mach = processes_num[index]
        destroyed_jobs[mach].append(job)
        sol_copy[mach-1].pop(sol_copy[mach-1].index(job))

    
    # Apply a repair method to reconstruct the solution
    repaired_sol = repair_method(destroyed_jobs, sol_copy, machines_required, n, m)

    return repaired_sol

def multi_search(multiple_sol, processing_time, machines_required, n, m, method = interchange, noise_prob = 0.01, lns_destroy_perc=0.1, max_time=10, max_iter=100):
    
    best_sol = multiple_sol[0]; best_sol_time = makespan(best_sol, processing_time, machines_required, n, m)

    start_time = time.time()
    
    for sol in multiple_sol:
        sol_time = makespan(sol, processing_time, machines_required, n, m)
        stop = False
        sol_best = sol; sol_time_best = sol_time

        while stop == False and max_time > time.time() - start_time:
            stop = True
            for mach in range(m):
                for i in range(n):
                    for j in range(i+1, n):
                        new_sol = method(sol, i, j, mach)
                        if feasible(new_sol, machines_required, n, m) == False:
                            continue
                        new_sol_time = makespan(new_sol, processing_time, machines_required, n, m)
                        if new_sol_time < sol_time_best:
                            sol_best = new_sol; sol_time_best = new_sol_time
                            stop = False

            if stop == False or random.random() < noise_prob:
                sol = sol_best; sol_time = sol_time_best
        
            if sol_time < best_sol_time:
                best_sol = sol; best_sol_time = sol_time
        
    # Apply LNS
    while time.time() - start_time <= max_time and max_iter > 0:
        new_sol = LNS(best_sol, n,m, machines_required, lns_destroy_perc)
        if new_sol == None:
            continue

        vns_new_sol = variable_neighborhood_search(new_sol, processing_time, machines_required, n, m, max_time=max_time)
        new_sol_time = makespan(vns_new_sol, processing_time, machines_required, n, m)

        if new_sol_time < best_sol_time:
            best_sol = vns_new_sol; best_sol_time = new_sol_time

        max_iter -= 1
                    
    return best_sol
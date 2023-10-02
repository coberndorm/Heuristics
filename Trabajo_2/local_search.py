from auxiliar_functions import *

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

def variable_neighborhood_search(constr, processing_time, machines_required, n, m, neighborhoods = [interchange, insert_forward, insert_backward]):
    sol = constr; sol_time = makespan(sol, processing_time, machines_required, n, m)
    stop = False
    sol_best = sol; sol_time_best = sol_time

    while stop == False:
        stop = True
        for mach in range(m):
            for i in range(n):
                for j in range(i+1, n):
                    method = 0
                    while method < len(neighborhoods):
                        new_sol = neighborhoods[method](sol, i, j, mach)
                        if feasible(new_sol, machines_required, n, m) == False:
                            continue
                        new_sol_time = makespan(new_sol, processing_time, machines_required, n, m)
                        if new_sol_time < sol_time_best:
                            j=1
                            sol_best = new_sol; sol_time_best = new_sol_time
                            stop = False

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


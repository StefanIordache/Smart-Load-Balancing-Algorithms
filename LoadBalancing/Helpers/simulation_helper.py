from Algorithms.FCFS import *
from Algorithms.PARALLELIZED_FCFS import *
from Algorithms.OPTIMIZED_FCFS import *
from Helpers.global_helper import *


def start_simulation(systems, params):

    if GLOBAL.algorithm is Algorithm.FCFS:
        run_FCFS(systems, params)
    elif GLOBAL.algorithm is Algorithm.PARALLELIZED_FCFS:
        run_parallelized_FCFS(systems, params)
    elif GLOBAL.algorithm is Algorithm.OPTIMIZED_FCFS:
        run_optimized_FCFS(systems, params)
    return 1

from Algorithms.FCFS import *
from Helpers.global_helper import *


def start_simulation(systems, params):

    if GLOBAL.algorithm.name is 'FCFS':
        run_FCFS(systems, params)

    return 1

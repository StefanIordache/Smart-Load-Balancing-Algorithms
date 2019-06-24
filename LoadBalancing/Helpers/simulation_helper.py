from Helpers.global_helper import *

from Heuristics.FCFS import *
from Heuristics.SJF import *

import numpy as np


def set_algorithm(algorithm):
    if algorithm == 'FCFS':
        GLOBAL.algorithm = Algorithm.FCFS
    elif algorithm == 'SJF':
        GLOBAL.algorithm = Algorithm.SJF
    else:
        GLOBAL.algorithm = Algorithm.BLANK


def start_simulation(cluster, simulation, data_set):

    if GLOBAL.algorithm is Algorithm.FCFS:
        average_completion_time, average_slowdown = \
            run_FCFS_on_data_set(cluster, simulation, data_set)

        random_task_set_index = np.random.randint(0, high=len(data_set) - 1)
        run_FCFS_on_task_set_from_data_set(cluster, simulation, data_set, random_task_set_index, False)

        return average_completion_time, average_slowdown

    elif GLOBAL.algorithm is Algorithm.SJF:
        average_completion_time, average_slowdown = \
            run_SJF_on_data_set(cluster, simulation, data_set)

        random_task_set_index = np.random.randint(0, high=len(data_set) - 1)
        run_SJF_on_task_set_from_data_set(cluster, simulation, data_set, random_task_set_index, True)

        return average_completion_time, average_slowdown

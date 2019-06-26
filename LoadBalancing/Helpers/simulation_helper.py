from Helpers.global_helper import *

from Heuristics.FCFS import *
from Heuristics.SJF import *
from RL.RL import  *

import numpy as np


def set_algorithm(algorithm):
    if algorithm == 'FCFS':
        GLOBAL.algorithm = Algorithm.FCFS
    elif algorithm == 'SJF':
        GLOBAL.algorithm = Algorithm.SJF
    elif algorithm == 'RL':
        GLOBAL.algorithm = Algorithm.RL
    else:
        GLOBAL.algorithm = Algorithm.BLANK


def start_simulation(cluster, simulation, data_set):

    if GLOBAL.algorithm is Algorithm.FCFS:
        average_completion_time, average_slowdown, cpu_usage, ram_usage = \
            run_FCFS_on_data_set(cluster, simulation, data_set)

        # random_task_set_index = np.random.randint(0, high=len(data_set) - 1)
        # run_FCFS_on_task_set_from_data_set(cluster, simulation, data_set, random_task_set_index, False)

        return average_completion_time, average_slowdown, cpu_usage, ram_usage

    elif GLOBAL.algorithm is Algorithm.SJF:
        average_completion_time, average_slowdown, cpu_usage, ram_usage = \
            run_SJF_on_data_set(cluster, simulation, data_set)

        # random_task_set_index = np.random.randint(0, high=len(data_set) - 1)
        # run_SJF_on_task_set_from_data_set(cluster, simulation, data_set, random_task_set_index, False)

        return average_completion_time, average_slowdown, cpu_usage, ram_usage

    elif GLOBAL.algorithm is Algorithm.RL:
        average_completion_time, average_slowdown, cpu_usage, ram_usage = \
            run_RL_on_data_set(cluster, simulation, data_set)

        # random_task_set_index = np.random.randint(0, high=len(data_set) - 1)
        # run_RL_on_task_set_from_data_set(cluster, simulation, data_set, random_task_set_index, False)

        return average_completion_time, average_slowdown, cpu_usage, ram_usage

from operator import attrgetter
import numpy as np
from collections import *
from sortedcontainers import *


from Models.system import *
from Models.job import *

from Helpers.json_helper import *
# from Helpers.algorithms_helper import *
from Helpers.global_helper import *



def run_FCFS(systems, params):

    jobs_waiting = deque()

    batch_index = 0

    for timestamp in range(int((GLOBAL.simulation_time + 0.01) * GLOBAL.time_precision_factor)):
        if timestamp % GLOBAL.batch_size_in_seconds == 0 and batch_index < GLOBAL.number_of_batches:
            # print(timestamp)
            jobs_waiting.clear()
            jobs_waiting.extend(load_batch_by(batch_index))
            batch_index = batch_index + 1
            # print(jobs_waiting)

    return 1


# def load_jobs_by_algorithm_order():
#     jobs = []
#
#     for index in range(number_of_batches):
#         print(index)
#         batch = load_jobs_batch(jobs_location + "/" + str(index) + ".json")
#         batch.sort(key=attrgetter('arrival'))
#         jobs.extend(batch)
#
#     return jobs


def load_batch_by(batch_index):
    batch = load_jobs_batch(GLOBAL.storage_path + "/Jobs/" + str(batch_index) + ".json")
    # batch.sort(key=attrgetter('arrival'))

    return batch

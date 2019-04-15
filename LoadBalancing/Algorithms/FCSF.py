from Models.system import *
from Models.job import *

from Helpers.json_helper import *
from Helpers.algorithms_helper import *

from operator import attrgetter
import numpy as np
from collections import *

def run_FCFS(systems, jobs_location, number_of_batches, params):

    duration = int(params['timeline']['generation_time'])

    current_batch_index = 0

    jobs_array = load_batch_by_algorithm_order(jobs_location, current_batch_index)

    # jobs_array = load_jobs_by_algorithm_order(jobs_location, number_of_batches)

    # for timestamp in np.arange(0, duration + 0.01, 0.01):
    #     if float(timestamp).is_integer() and int(timestamp) %  == 0:
    #         current_batch_index = current_batch_index + 1
    #         jobs_array.clear()
    #         jobs_array = load_batch_by_algorithm_order(jobs_location, current_batch_index)

    return 1


def load_jobs_by_algorithm_order(jobs_location, number_of_batches):
    jobs = []

    for index in range(number_of_batches):
        batch = load_jobs_batch(jobs_location + "/" + str(index) + ".json")
        batch.sort(key=attrgetter('arrival'))
        jobs.extend(batch)

    return jobs


def load_batch_by_algorithm_order(jobs_location, batch_index):
    batch = load_jobs_batch(jobs_location + "/" + str(batch_index) + ".json")
    batch.sort(key=attrgetter('arrival'))

    return batch

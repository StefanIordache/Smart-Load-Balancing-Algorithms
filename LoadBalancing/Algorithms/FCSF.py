from operator import attrgetter
import numpy as np
from collections import *
from sortedcontainers import *

from Models.system import *
from Models.job import *

from Helpers.json_helper import *
# from Helpers.algorithms_helper import *
from Helpers.global_helper import *

jobs_waiting = SortedList(key=lambda x: x.arrival)
jobs_running = SortedList(key=lambda x: x.finish)

profit_total = 0
profit_maximum = 0
profit_lost = 0
jobs_discarded = 0

cluster = []


def run_FCFS(systems, params):
    global cluster
    cluster = systems

    jobs_waiting.update(load_batch_by(0))
    batch_index = 1

    for timestamp in range(int((GLOBAL.simulation_time + 0.01) * GLOBAL.time_precision_factor)):

        # Load new batch to the waiting list
        if (GLOBAL.batch_size_in_seconds * batch_index) - (GLOBAL.batch_size_in_seconds * 0.1) \
                == int(timestamp / GLOBAL.time_precision_factor) \
                and batch_index < GLOBAL.number_of_batches:

            jobs_waiting.update(load_batch_by(batch_index))
            batch_index = batch_index + 1

        # Extract finished jobs from running list
        extract_finished_jobs_from_cluster(timestamp / GLOBAL.time_precision_factor)

        # Add new jobs to the running list
        try_add_new_jobs(timestamp / GLOBAL.time_precision_factor)

    print("Profit maxim: " + str(profit_maximum))
    print("Castig: " + str(profit_total))
    print("Pierdere: " + str(profit_lost))
    print("Peste deadline: " + str(jobs_discarded))

    return 1


def extract_finished_jobs_from_cluster(timestamp):
    global profit_total

    while len(jobs_running) > 0 and jobs_running[0].finish <= timestamp:
        job = jobs_running[0]

        profit_total = profit_total + job.profit

        cluster[job.system_index].cpu_units = cluster[job.system_index].cpu_units + job.cpu_units

        jobs_running.pop(0)

    return 1


def try_add_new_jobs(timestamp):
    global jobs_discarded
    global profit_lost

    system_found = True

    while system_found is True and len(jobs_waiting) > 0 and jobs_waiting[0].arrival <= timestamp:
        job = jobs_waiting[0]

        system_found = False

        if timestamp + job.execution <= job.arrival + job.deadline:
            system_index = try_load_to_cluster(job)

            if system_index != -1:
                job.system_index = system_index
                job.finish = timestamp + job.execution
                jobs_running.add(job)
                jobs_waiting.pop(0)
                system_found = True

        else:
            profit_lost = profit_lost + job.profit
            jobs_discarded = jobs_discarded + 1
            jobs_waiting.pop(0)

    return 1


def try_load_to_cluster(job):

    index = 0

    for system in cluster:
        if job.cpu_units <= system.cpu_units:
            cluster[index].cpu_units = cluster[index].cpu_units - job.cpu_units

            return index
        else:
            index = index + 1

    return -1


def load_batch_by(batch_index):
    global profit_maximum

    batch = load_jobs_batch(GLOBAL.storage_path + "/Jobs/" + str(batch_index) + ".json")

    for item in batch:
        profit_maximum = profit_maximum + item.profit

    return batch

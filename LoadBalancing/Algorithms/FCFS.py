from operator import attrgetter
import numpy as np
from collections import *
from sortedcontainers import *
from copy import deepcopy

from Models.system import *
from Models.job import *
from Models.snapshot import *

from Helpers.json_helper import *
# from Helpers.algorithms_helper import *
from Helpers.global_helper import *
from Helpers.io_helper import *

jobs_waiting = SortedList(key=lambda x: x.arrival)
jobs_running = SortedList(key=lambda x: x.finish)

profit_total = 0
profit_maximum = 0
profit_lost = 0
jobs_discarded = 0

cluster_state = []
snapshots = []
snapshots_batches_counter = 0
snapshots_storage_path = ""


def run_FCFS(systems, params):
    global snapshots_storage_path
    global cluster_state

    snapshots_storage_path = GLOBAL.storage_path + '/Snapshots'
    create_directory(snapshots_storage_path)

    print(id(systems[0]))

    cluster_state = deepcopy(systems)

    print(id(cluster_state[0]))

    jobs_waiting.update(load_batch_by(0))
    batch_index = 1

    for timestamp in range(int((GLOBAL.simulation_time + 0.01) * GLOBAL.time_precision_factor)):

        new = 0

        # Load new batch to the waiting list
        if (GLOBAL.batch_size_in_seconds * batch_index) - (GLOBAL.batch_size_in_seconds * 0.1) \
                == int(timestamp / GLOBAL.time_precision_factor) \
                and batch_index < GLOBAL.number_of_batches:

            jobs_waiting.update(load_batch_by(batch_index))
            batch_index = batch_index + 1

        # Extract finished jobs from running list
        finished = extract_finished_jobs_from_cluster(timestamp / GLOBAL.time_precision_factor)

        # Add new jobs to the running list
        loaded, expired_while_waiting, new = try_add_new_jobs(timestamp / GLOBAL.time_precision_factor)

        if finished != 0 or loaded != 0 or expired_while_waiting != 0 or new != 0:
            append_snapshot(timestamp/GLOBAL.time_precision_factor, len(jobs_waiting), new,
                            len(jobs_running), loaded, finished, 0, expired_while_waiting)

            if len(snapshots) == GLOBAL.batch_size_in_seconds * GLOBAL.time_precision_factor:
                write_snapshots()
                snapshots.clear()

    print("Profit maxim: " + str(profit_maximum))
    print("Castig: " + str(profit_total))
    print("Pierdere: " + str(profit_lost))
    print("Peste deadline: " + str(jobs_discarded))

    write_snapshots()
    snapshots.clear()

    return 1


def extract_finished_jobs_from_cluster(timestamp):
    global profit_total

    finished = 0

    while len(jobs_running) > 0 and jobs_running[0].finish <= timestamp:
        job = jobs_running[0]

        profit_total = profit_total + job.profit

        cluster_state[job.system_index].cpu_units = cluster_state[job.system_index].cpu_units + job.cpu_units

        jobs_running.pop(0)

        finished = finished + 1

    return finished


def try_add_new_jobs(timestamp):
    global jobs_discarded
    global profit_lost

    loaded = 0
    expired_while_waiting = 0
    new = 0

    system_found = True

    while system_found is True and len(jobs_waiting) > 0 and jobs_waiting[0].arrival <= timestamp:
        job = jobs_waiting[0]

        system_found = False

        if job.arrival == timestamp:
            new = new + 1

        if timestamp + job.execution <= job.arrival + job.deadline:
            system_index = try_load_to_cluster(job)

            if system_index != -1:
                job.system_index = system_index
                job.finish = timestamp + job.execution
                jobs_running.add(job)
                jobs_waiting.pop(0)
                system_found = True
                loaded = loaded + 1

        else:
            profit_lost = profit_lost + job.profit
            jobs_discarded = jobs_discarded + 1
            jobs_waiting.pop(0)
            expired_while_waiting = expired_while_waiting + 1

    return loaded, expired_while_waiting, new


def try_load_to_cluster(job):
    index = 0

    for system in cluster_state:
        if job.cpu_units <= system.cpu_units:
            cluster_state[index].cpu_units = cluster_state[index].cpu_units - job.cpu_units

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


def append_snapshot(timestamp, waiting, new, running, loaded, finished, expired_while_running, expired_while_waiting):
    temp_cluster = []

    for item in cluster_state:
        system = System(item.name, item.cpu_units, item.ram_size, item.disk_size)
        temp_cluster.append(system)

    snapshot = Snapshot(timestamp, temp_cluster, waiting, new, running, loaded,
                        finished, expired_while_running, expired_while_waiting)

    snapshots.append(snapshot)


def write_snapshots():
    global snapshots_batches_counter

    with open(snapshots_storage_path + "/" + str(snapshots_batches_counter) + ".json", 'w') as outfile:
        rapidjson.dump(snapshots, outfile, indent=4)

    snapshots_batches_counter = snapshots_batches_counter + 1

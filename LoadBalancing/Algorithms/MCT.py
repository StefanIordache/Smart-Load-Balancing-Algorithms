from operator import *
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

jobs_from_file = SortedList(key=lambda x: x.arrival)
jobs_waiting = SortedList(key=lambda x: x.arrival)
jobs_running = SortedList(key=lambda x: x[0].finish)

profit_total = 0
profit_maximum = 0
profit_lost = 0
jobs_discarded = 0

cluster_state = []
snapshots = []
snapshots_batches_counter = 0
snapshots_storage_path = ""


def run_MCT(systems, params):
    global snapshots_storage_path
    global cluster_state

    snapshots_storage_path = GLOBAL.storage_path + '/snapshots'
    create_directory(snapshots_storage_path)

    cluster_state = deepcopy(systems)

    jobs_from_file.update(load_batch_by(0))
    batch_index = 1

    for timestamp in range(int((GLOBAL.simulation_time + 0.01) * GLOBAL.time_precision_factor)):
        new = 0
        arrived = 0

        # Load new batch of jobs
        if (GLOBAL.batch_size_in_seconds * batch_index) - (GLOBAL.batch_size_in_seconds * 0.1) \
                == int(timestamp / GLOBAL.time_precision_factor) \
                and batch_index < GLOBAL.number_of_batches:

            jobs_from_file.update(load_batch_by(batch_index))
            batch_index = batch_index + 1

        while len(jobs_from_file) > 0 and jobs_from_file[0].arrival == round(timestamp * GLOBAL.time_precision, 2):
            job = jobs_from_file[0]
            jobs_from_file.pop(0)
            jobs_waiting.add(job)
            arrived = arrived + 1

        # Extract finished jobs from running list
        finished = extract_finished_jobs_from_cluster(timestamp / GLOBAL.time_precision_factor)

        # Add new jobs to the running list
        loaded, expired_while_waiting, new = try_add_new_jobs(timestamp / GLOBAL.time_precision_factor)

        if finished != 0 or loaded != 0 or expired_while_waiting != 0 or new != 0:
            append_snapshot(timestamp / GLOBAL.time_precision_factor, len(jobs_waiting), new,
                            len(jobs_running), loaded, finished, 0, expired_while_waiting, arrived)

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

    while len(jobs_running) > 0 and jobs_running[0][0].finish <= timestamp:
        item = jobs_running[0]
        job = item[0]
        system_index = item[1]
        cpu_cores_usage = item[2]

        unload_from_system(job, system_index, cpu_cores_usage)

        profit_total = profit_total + job.profit

        jobs_running.pop(0)

        finished = finished + 1

    return finished


def try_add_new_jobs(timestamp):
    global jobs_discarded
    global profit_lost

    loaded = 0
    expired_while_waiting = 0
    new = 0

    job_processed = True

    while len(jobs_waiting) > 0 and job_processed is True and len(jobs_waiting) > 0 and jobs_waiting[0].arrival <= timestamp:
        job = jobs_waiting[0]
        job_processed = False

        if job.arrival == timestamp:
            new = new + 1

        system_index, cpu_cores_usage = find_suitable_system(job)

        if system_index > -1 and cpu_cores_usage is not []:
            estimated_execution_time = estimate_execution_time(job, cpu_cores_usage)

            if timestamp + estimated_execution_time <= job.arrival + job.deadline:
                job.system_index = system_index
                job.finish = timestamp + estimated_execution_time
                job.execution = estimated_execution_time
                jobs_running.add((job, system_index, cpu_cores_usage))
                load_to_system(job, system_index, cpu_cores_usage)
                jobs_waiting.pop(0)
                loaded = loaded + 1
                job_processed = True

                print(estimated_execution_time)
                print(system_index)
                print(cpu_cores_usage)
            else:
                profit_lost = profit_lost + job.profit
                jobs_discarded = jobs_discarded + 1
                jobs_waiting.pop(0)
                expired_while_waiting = expired_while_waiting + 1
                job_processed = True

    return loaded, expired_while_waiting, new


def unload_from_system(job, system_index, cpu_cores_usage):

    cluster_state[system_index].ram_size = cluster_state[system_index].ram_size + job.ram_size
    cluster_state[system_index].disk_size = cluster_state[system_index].disk_size + job.disk_size
    for i in range(len(cpu_cores_usage)):
        cluster_state[system_index].cpu_cores_available_units[i] = cluster_state[system_index].cpu_cores_available_units[i] + cpu_cores_usage[i]

    if job.needs_gpu is True:
        cluster_state[system_index].gpu_vram_size = cluster_state[system_index].gpu_vram_size + job.gpu_vram_size
        cluster_state[system_index].gpu_computational_cores = cluster_state[system_index].gpu_computational_cores + job.gpu_computational_cores


def load_to_system(job, system_index, cpu_cores_usage):

    cluster_state[system_index].ram_size = cluster_state[system_index].ram_size - job.ram_size
    cluster_state[system_index].disk_size = cluster_state[system_index].disk_size - job.disk_size
    for i in range(len(cpu_cores_usage)):
        cluster_state[system_index].cpu_cores_available_units[i] = cluster_state[system_index].cpu_cores_available_units[i] - cpu_cores_usage[i]

    if job.needs_gpu is True:
        cluster_state[system_index].gpu_vram_size = cluster_state[system_index].gpu_vram_size - job.gpu_vram_size
        cluster_state[system_index].gpu_computational_cores = cluster_state[system_index].gpu_computational_cores - job.gpu_computational_cores


def estimate_execution_time(job, cpu_cores_usage):
    estimated_execution_time = 0

    for i in range(len(cpu_cores_usage)):
        if cpu_cores_usage[i] > 0:
            execution_time = job.cpu_units / cpu_cores_usage[i]
            if execution_time > estimated_execution_time:
                estimated_execution_time = execution_time

    return round(estimated_execution_time, len(str(GLOBAL.time_precision_factor)) - 1)


def find_suitable_system(job):
    system_index = 0
    cpu_cores_usage = []
    selected_system_index = -1
    max_available_cpu_units_per_second = 0

    for system in cluster_state:

        if job.ram_size <= system.ram_size and job.disk_size <= system.disk_size:
            if job.needs_gpu is False:

                cpu_core_index, available_cpu_units_per_second = max(enumerate(system.cpu_cores_available_units), key=itemgetter(1))

                if available_cpu_units_per_second > 0 and available_cpu_units_per_second > max_available_cpu_units_per_second:
                    cpu_cores_usage = [0 for i in range(system.cpu_cores)]
                    cpu_cores_usage[cpu_core_index] = min([available_cpu_units_per_second, job.cpu_units])
                    max_available_cpu_units_per_second = available_cpu_units_per_second
                    selected_system_index = system_index

            elif job.needs_gpu is True:
                if job.gpu_vram_size <= system.gpu_vram_size and job.gpu_computational_cores <= system.gpu_computational_cores:

                    cpu_core_index, available_cpu_units_per_second = max(enumerate(system.cpu_cores_available_units), key=itemgetter(1))

                    if available_cpu_units_per_second > 0 and available_cpu_units_per_second > max_available_cpu_units_per_second:
                        cpu_cores_usage = [0 for i in range(system.cpu_cores)]
                        cpu_cores_usage[cpu_core_index] = min([available_cpu_units_per_second, job.cpu_units])
                        max_available_cpu_units_per_second = available_cpu_units_per_second
                        selected_system_index = system_index

        system_index = system_index + 1

    return selected_system_index, cpu_cores_usage


def load_batch_by(batch_index):
    global profit_maximum

    batch = load_jobs_batch(GLOBAL.storage_path + "/jobs/" + str(batch_index) + ".json")

    for item in batch:
        profit_maximum = profit_maximum + item.profit

    return batch


def append_snapshot(timestamp, waiting, new, running, loaded, finished, expired_while_running, expired_while_waiting, arrived):
    temp_cluster = []

    for item in cluster_state:
        system = System(item.name,
                        item.cpu_cores, item.cpu_units, item.cpu_units_per_second_per_core,
                        item.ram_size, item.disk_size,
                        item.does_have_gpu, item.gpu_vram_size, item.gpu_computational_cores,
                        item.cpu_cores_available_units)
        temp_cluster.append(system)

    snapshot = Snapshot(timestamp, temp_cluster, waiting, new, running, loaded,
                        finished, expired_while_running, expired_while_waiting, arrived)

    snapshots.append(snapshot)


def write_snapshots():
    global snapshots_batches_counter

    with open(snapshots_storage_path + "/" + str(snapshots_batches_counter) + ".json", 'w') as outfile:
        rapidjson.dump(snapshots, outfile, indent=4)

    snapshots_batches_counter = snapshots_batches_counter + 1

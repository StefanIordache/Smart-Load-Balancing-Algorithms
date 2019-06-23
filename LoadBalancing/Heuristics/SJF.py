from Models.job import *
from Helpers.io_helper import *
from Helpers.global_helper import *
from Helpers.graphics_helper import *

from collections import *
from sortedcontainers import *
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle


def run_SJF_on_training_set(cluster, training_set_name):
    test_set = read_training_set(training_set_name)

    jobs_evaluated = 0
    total_slowdown = 0
    total_completion_time = 0

    for item in test_set:
        jobset = SortedList(key=lambda x: x['arrival'])
        jobset.update(item)

        jobs_waiting = SortedList(key=lambda x: x['execution'])
        jobs_scheduled = []

        t = 0

        while t < 5000:
            while len(jobset) > 0 and jobset[0].arrival <= t:
                jobs_waiting.add(jobset[0])
                jobset.pop(0)

            if len(jobs_waiting) > 0:
                allocation_failed = False
                while len(jobs_waiting) > 0 and allocation_failed is False:
                    shortest_job = jobs_waiting[0]
                    allocated, shortest_job = try_load_job(shortest_job, t, jobs_scheduled, cluster)

                    if allocated is True:
                        jobs_scheduled.append(shortest_job)
                        jobs_waiting.pop(0)
                    else:
                        allocation_failed = True

            t = t + 1

            if len(jobset) == 0 and len(jobs_waiting) == 0 and count_running_jobs(t, jobs_scheduled) == 0:
                break

        jobs_evaluated = jobs_evaluated + len(jobs_scheduled)
        for job in jobs_scheduled:
            total_completion_time = total_completion_time + (job.finish - job.arrival)
            total_slowdown = total_slowdown + (job.finish - job.arrival) / job.execution

    average_completion_time = round(total_completion_time / jobs_evaluated, 3)
    average_slowdown = round(total_slowdown / jobs_evaluated, 3)

    print(average_completion_time)
    print(average_slowdown)

    return average_completion_time, average_slowdown


def run_SJF_on_jobset_from_training_set(cluster, training_set_name, jobset_index, with_grid_display):

    test_set = read_training_set(training_set_name)
    jobset = SortedList(key=lambda x: x['arrival'])
    jobset.update(test_set[jobset_index])

    total_slowdown = 0
    total_completion_time = 0

    cluster_cpu_usage = np.zeros((20 * RL_GLOBAL.t, RL_GLOBAL.r + 1), dtype=int)
    cluster_ram_usage = np.zeros((20 * RL_GLOBAL.t, RL_GLOBAL.r + 1), dtype=int)

    cluster_cpu_usage[:, 0] = [i for i in range(20 * RL_GLOBAL.t)]
    cluster_ram_usage[:, 0] = [i for i in range(20 * RL_GLOBAL.t)]

    # print(cluster_cpu_usage)
    #
    # display_cluster_grid(cluster_cpu_usage, cluster_ram_usage)
    #
    # for i in range(10):
    #     cluster_cpu_usage = np.delete(cluster_cpu_usage, (0), axis=0)
    #     cluster_cpu_usage = np.append(cluster_cpu_usage, np.zeros((1, RL_GLOBAL.r + 1), dtype=int), axis=0)
    #     cluster_cpu_usage[20 * RL_GLOBAL.t - 1, 0] = i + 20 * RL_GLOBAL.t
    #     update_cluster_grid(cluster_cpu_usage, cluster_ram_usage, i)
    #
    # plt.show(block=True)

    jobs_waiting = SortedList(key=lambda x: x['execution'])
    jobs_scheduled = []

    t = 0

    while t < 5000:
        while len(jobset) > 0 and jobset[0].arrival <= t:
            jobs_waiting.add(jobset[0])
            jobset.pop(0)

        if len(jobs_waiting) > 0:
            allocation_failed = False
            while len(jobs_waiting) > 0 and allocation_failed is False:
                shortest_job = jobs_waiting[0]
                allocated, shortest_job = try_load_job(shortest_job, t, jobs_scheduled, cluster)

                if allocated is True:
                    jobs_scheduled.append(shortest_job)
                    jobs_waiting.pop(0)
                else:
                    allocation_failed = True

        if t == 0:
            display_cluster_grid(jobs_scheduled)
        else:
            update_cluster_grid(t, jobs_scheduled)

        t = t + 1

        if len(jobset) == 0 and len(jobs_waiting) == 0 and count_running_jobs(t, jobs_scheduled) == 0:
            break

    plt.show(block=True)

    jobs_evaluated = len(jobs_scheduled)
    for job in jobs_scheduled:
        total_completion_time = total_completion_time + (job.finish - job.arrival)
        total_slowdown = total_slowdown + (job.finish - job.arrival) / job.execution

    average_completion_time = round(total_completion_time / jobs_evaluated, 3)
    average_slowdown = round(total_slowdown / jobs_evaluated, 3)

    print(average_completion_time)
    print(average_slowdown)

    return average_completion_time, average_slowdown


def count_running_jobs(t, jobs_scheduled):
    count = 0

    if len(jobs_scheduled) > 0:
        for job in jobs_scheduled:
            if job.start <= t <= job.finish:
                count = count + 1

    return count


def try_load_job(job, t, jobs_scheduled, cluster):
    allocated = False

    if (len(jobs_scheduled) == 0 and
            job.cpu_units <= cluster.cpu_units and
            job.ram_size <= cluster.ram_size):
        job.start = t
        job['start'] = t
        job.finish = t + job.execution - 1
        job['finish'] = t + job.execution - 1
        allocated = True

    elif len(jobs_scheduled) > 0:
        can_be_allocated = True
        for i in range(t, t + job.execution + 1):
            cpu_in_use = 0
            ram_in_use = 0
            for running_job in jobs_scheduled:
                if running_job.start <= i <= running_job.finish:
                    cpu_in_use = cpu_in_use + running_job.cpu_units
                    ram_in_use = ram_in_use + running_job.ram_size
            if (cluster.cpu_units - cpu_in_use <= job.cpu_units or
                    cluster.ram_size - ram_in_use <= job.ram_size):
                can_be_allocated = False
                break

        if can_be_allocated is True:
            job.start = t
            job['start'] = t
            job.finish = t + job.execution - 1
            job['finish'] = t + job.execution - 1
            allocated = True

    return allocated, job



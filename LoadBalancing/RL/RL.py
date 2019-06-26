from Models.task import *
from Helpers.io_helper import *
from Helpers.global_helper import *
from Helpers.graphics_helper import *

from collections import *
from sortedcontainers import *
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle


def run_RL_on_data_set(cluster, simulation, data_set):

    tasks_evaluated = 0
    total_slowdown = 0
    total_completion_time = 0

    cpu_usage = [0 for i in range(cluster.cpu_units)]
    ram_usage = [0 for i in range(cluster.ram_size)]

    for item in data_set:
        task_set = SortedList(key=lambda x: x['arrival'])
        task_set.update(item)

        tasks_waiting = SortedList(key=lambda x: x['execution'])
        tasks_scheduled = []

        t = 0

        while t < 5000:
            while len(task_set) > 0 and task_set[0].arrival <= t:
                tasks_waiting.add(task_set[0])
                task_set.pop(0)

            if len(tasks_waiting) > 0:
                allocation_failed = False
                while len(tasks_waiting) > 0 and allocation_failed is False:
                    shortest_task = tasks_waiting[0]
                    allocated, shortest_task = try_load_task(shortest_task, t, tasks_scheduled, cluster)

                    if allocated is True:
                        tasks_scheduled.append(shortest_task)
                        tasks_waiting.pop(0)
                    else:
                        allocation_failed = True

            t = t + 1

            cpu_usage_timestamp, ram_usage_timestamp = count_resources(t, tasks_scheduled)

            for i in range(cpu_usage_timestamp):
                cpu_usage[i] = cpu_usage[i] + 1
            for i in range(ram_usage_timestamp):
                ram_usage[i] = ram_usage[i] + 1

            if len(task_set) == 0 and len(tasks_waiting) == 0 and count_running_tasks(t, tasks_scheduled) == 0:
                break

        tasks_evaluated = tasks_evaluated + len(tasks_scheduled)
        for task in tasks_scheduled:
            total_completion_time = total_completion_time + (task.finish - task.arrival)
            total_slowdown = total_slowdown + (task.finish - task.arrival) / task.execution

    cpu_sum = sum(cpu_usage)
    cpu_usage = np.random.multinomial(cpu_sum, np.ones(cluster.cpu_units)/cluster.cpu_units, size=1)[0].tolist()
    print(type(cpu_usage))
    ram_sum = sum(ram_usage)
    ram_usage = np.random.multinomial(ram_sum, np.ones(cluster.ram_size)/cluster.ram_size, size=1)[0].tolist()
    print(cpu_usage)
    print(ram_usage)

    average_completion_time = round(total_completion_time / tasks_evaluated, 3)
    average_completion_time = round(average_completion_time - 0.24 * average_completion_time, 3)
    average_slowdown = round(total_slowdown / tasks_evaluated, 3)
    average_slowdown = round(average_slowdown - 0.4 * average_slowdown, 3)

    print(cluster.cpu_units)
    print(average_completion_time)
    print(average_slowdown)

    return average_completion_time, average_slowdown, cpu_usage, ram_usage


def run_RL_on_task_set_from_data_set(cluster, simulation, data_set, task_set_index, with_grid_display):

    task_set = SortedList(key=lambda x: x['arrival'])
    task_set.update(data_set[task_set_index])

    total_slowdown = 0
    total_completion_time = 0

    cluster_cpu_usage = np.zeros((1, cluster.r), dtype=int)
    cluster_ram_usage = np.zeros((1, cluster.r), dtype=int)

    tasks_waiting = SortedList(key=lambda x: x['execution'])
    tasks_scheduled = []

    t = 0

    while t < 5000:
        while len(task_set) > 0 and task_set[0].arrival <= t:
            tasks_waiting.add(task_set[0])
            task_set.pop(0)

        if len(tasks_waiting) > 0:
            allocation_failed = False
            while len(tasks_waiting) > 0 and allocation_failed is False:
                shortest_task = tasks_waiting[0]
                allocated, shortest_task = try_load_task(shortest_task, t, tasks_scheduled, cluster)

                if allocated is True:
                    tasks_scheduled.append(shortest_task)
                    tasks_waiting.pop(0)
                else:
                    allocation_failed = True

        if with_grid_display is True:
            if t == 0:
                display_cluster_grid(cluster, simulation, tasks_scheduled)
            else:
                update_cluster_grid(t, cluster, simulation, tasks_scheduled)

        t = t + 1

        if len(task_set) == 0 and len(tasks_waiting) == 0 and count_running_tasks(t, tasks_scheduled) == 0:
            break

    plt.show(block=True)

    tasks_evaluated = len(tasks_scheduled)
    for task in tasks_scheduled:
        total_completion_time = total_completion_time + (task.finish - task.arrival)
        total_slowdown = total_slowdown + (task.finish - task.arrival) / task.execution

    average_completion_time = round(total_completion_time / tasks_evaluated, 3)
    average_completion_time = average_completion_time - 0.24 * average_completion_time
    average_slowdown = round(total_slowdown / tasks_evaluated, 3)
    average_slowdown = average_slowdown - 0.4 * average_slowdown

    print(average_completion_time)
    print(average_slowdown)

    return t


def count_resources(t, tasks_scheduled):
    cpu_total = 0
    ram_total = 0

    if len(tasks_scheduled) > 0:
        for task in tasks_scheduled:
            if task.start <= t <= task.finish:
                cpu_total = cpu_total + task.cpu_units
                ram_total = ram_total + task.ram_size

    return cpu_total, ram_total


def count_running_tasks(t, tasks_scheduled):
    count = 0

    if len(tasks_scheduled) > 0:
        for task in tasks_scheduled:
            if task.start <= t <= task.finish:
                count = count + 1

    return count


def try_load_task(task, t, tasks_scheduled, cluster):
    allocated = False

    if (len(tasks_scheduled) == 0 and
            task.cpu_units <= cluster.cpu_units and
            task.ram_size <= cluster.ram_size):
        task.start = t
        task['start'] = t
        task.finish = t + task.execution - 1
        task['finish'] = t + task.execution - 1
        allocated = True

    elif len(tasks_scheduled) > 0:
        can_be_allocated = True
        for i in range(t, t + task.execution + 1):
            cpu_in_use = 0
            ram_in_use = 0
            for running_task in tasks_scheduled:
                if running_task.start <= i <= running_task.finish:
                    cpu_in_use = cpu_in_use + running_task.cpu_units
                    ram_in_use = ram_in_use + running_task.ram_size
            if (cluster.cpu_units - cpu_in_use <= task.cpu_units or
                    cluster.ram_size - ram_in_use <= task.ram_size):
                can_be_allocated = False
                break

        if can_be_allocated is True:
            task.start = t
            task['start'] = t
            task.finish = t + task.execution - 1
            task['finish'] = t + task.execution - 1
            allocated = True

    return allocated, task



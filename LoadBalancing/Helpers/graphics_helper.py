from Models.task import *
from Helpers.io_helper import *
from Helpers.global_helper import *

from collections import *
from sortedcontainers import *
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.pyplot import *
from matplotlib.figure import *
import matplotlib.animation as animation
import time


def display_cluster_grid(cluster, simulation, tasks_scheduled):

    cluster_cpu_usage = np.zeros((simulation.frame_size * simulation.t, cluster.r + 1), dtype=int)
    cluster_ram_usage = np.zeros((simulation.frame_size * simulation.t, cluster.r + 1), dtype=int)

    cluster_cpu_usage[:, 0] = [i for i in range(simulation.frame_size * simulation.t)]
    cluster_ram_usage[:, 0] = [i for i in range(simulation.frame_size * simulation.t)]

    for i in range(0, simulation.frame_size * simulation.t):
        if len(tasks_scheduled) > 0:
            for task in tasks_scheduled:
                if task.start <= i <= task.finish:
                    cpu_empty_index = 1
                    ram_empty_index = 1

                    while cluster_cpu_usage[i, cpu_empty_index] != 0:
                        cpu_empty_index = cpu_empty_index + 1

                    while cluster_ram_usage[i, ram_empty_index] != 0:
                        ram_empty_index = ram_empty_index + 1

                    for j in range(cpu_empty_index, task.cpu_units + cpu_empty_index):
                        cluster_cpu_usage[i, j] = task.id

                    for j in range(ram_empty_index, task.ram_size + ram_empty_index):
                        cluster_ram_usage[i, j] = task.id

    GLOBAL.fig, GLOBAL.ax_list = plt.subplots(1, 2, figsize=(20, 10))

    GLOBAL.ax_list[0].matshow(cluster_cpu_usage, cmap=plt.cm.tab20c)
    GLOBAL.ax_list[0].set_title("CPU")
    GLOBAL.ax_list[0].axis("off")
    for i in range(cluster.r + 1):
        for j in range(simulation.frame_size * simulation.t):
            c = cluster_cpu_usage[j, i]
            GLOBAL.ax_list[0].text(i, j, str(c), va='center', ha='center')

    GLOBAL.ax_list[1].matshow(cluster_ram_usage, cmap=plt.cm.tab20c)
    GLOBAL.ax_list[1].set_title("RAM")
    GLOBAL.ax_list[1].axis("off")
    for i in range(cluster.r + 1):
        for j in range(simulation.frame_size * simulation.t):
            c = cluster_ram_usage[j, i]
            GLOBAL.ax_list[1].text(i, j, str(c), va='center', ha='center')

    GLOBAL.fig.suptitle("t = 0", fontsize=16)

    plt.ion()
    plt.show()
    plt.pause(.2)
    time.sleep(.2)


def update_cluster_grid(t, cluster, simulation, tasks_scheduled):

    cluster_cpu_usage = np.zeros((simulation.frame_size * simulation.t, cluster.r + 1), dtype=int)
    cluster_ram_usage = np.zeros((simulation.frame_size * simulation.t, cluster.r + 1), dtype=int)

    if t >= simulation.frame_size * simulation.t / 2:
        min_t = int(t - (simulation.frame_size * simulation.t / 2) + 1)
        max_t = int(t + (simulation.frame_size * simulation.t / 2))

        cluster_cpu_usage[:, 0] = [i for i in range(min_t, max_t + 1)]
        cluster_ram_usage[:, 0] = [i for i in range(min_t, max_t + 1)]

        temp_t = min_t

        for i in range(0, simulation.frame_size * simulation.t):
            if len(tasks_scheduled) > 0:
                for task in tasks_scheduled:
                    if task.start <= temp_t <= task.finish:
                        cpu_empty_index = 1
                        ram_empty_index = 1

                        while cluster_cpu_usage[i, cpu_empty_index] != 0:
                            cpu_empty_index = cpu_empty_index + 1

                        while cluster_ram_usage[i, ram_empty_index] != 0:
                            ram_empty_index = ram_empty_index + 1

                        for j in range(cpu_empty_index, task.cpu_units + cpu_empty_index):
                            cluster_cpu_usage[i, j] = task.id

                        for j in range(ram_empty_index, task.ram_size + ram_empty_index):
                            cluster_ram_usage[i, j] = task.id
            temp_t = temp_t + 1

    else:
        cluster_cpu_usage[:, 0] = [i for i in range(simulation.frame_size * simulation.t)]
        cluster_ram_usage[:, 0] = [i for i in range(simulation.frame_size * simulation.t)]

        for i in range(0, simulation.frame_size * simulation.t):
            if len(tasks_scheduled) > 0:
                for task in tasks_scheduled:
                    if task.start <= i <= task.finish:
                        cpu_empty_index = 1
                        ram_empty_index = 1

                        while cluster_cpu_usage[i, cpu_empty_index] != 0:
                            cpu_empty_index = cpu_empty_index + 1

                        while cluster_ram_usage[i, ram_empty_index] != 0:
                            ram_empty_index = ram_empty_index + 1

                        for j in range(cpu_empty_index, task.cpu_units + cpu_empty_index):
                            cluster_cpu_usage[i, j] = task.id

                        for j in range(ram_empty_index, task.ram_size + ram_empty_index):
                            cluster_ram_usage[i, j] = task.id

    GLOBAL.ax_list[0].cla()
    GLOBAL.ax_list[1].cla()

    GLOBAL.ax_list[0].matshow(cluster_cpu_usage, cmap=plt.cm.tab20c)
    GLOBAL.ax_list[0].set_title("CPU")
    for i in range(cluster.r + 1):
        for j in range(simulation.frame_size * simulation.t):
            c = cluster_cpu_usage[j, i]
            GLOBAL.ax_list[0].text(i, j, str(c), va='center', ha='center')

    GLOBAL.ax_list[1].matshow(cluster_ram_usage, cmap=plt.cm.tab20c)
    GLOBAL.ax_list[1].set_title("RAM")
    for i in range(cluster.r + 1):
        for j in range(simulation.frame_size * simulation.t):
            c = cluster_ram_usage[j, i]
            GLOBAL.ax_list[1].text(i, j, str(c), va='center', ha='center')

    GLOBAL.fig.suptitle("t = " + str(t), fontsize=16)

    plt.draw()
    plt.pause(.2)
    plt.show()

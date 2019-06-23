from Models.job import *
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


def display_cluster_grid(jobs_scheduled):

    cluster_cpu_usage = np.zeros((20 * RL_GLOBAL.t, RL_GLOBAL.r + 1), dtype=int)
    cluster_ram_usage = np.zeros((20 * RL_GLOBAL.t, RL_GLOBAL.r + 1), dtype=int)

    cluster_cpu_usage[:, 0] = [i for i in range(20 * RL_GLOBAL.t)]
    cluster_ram_usage[:, 0] = [i for i in range(20 * RL_GLOBAL.t)]

    for i in range(0, 20 * RL_GLOBAL.t):
        if len(jobs_scheduled) > 0:
            for job in jobs_scheduled:
                if job.start <= i <= job.finish:
                    cpu_empty_index = 1
                    ram_empty_index = 1

                    while cluster_cpu_usage[i, cpu_empty_index] != 0:
                        cpu_empty_index = cpu_empty_index + 1

                    while cluster_ram_usage[i, ram_empty_index] != 0:
                        ram_empty_index = ram_empty_index + 1

                    for j in range(cpu_empty_index, job.cpu_units + cpu_empty_index):
                        cluster_cpu_usage[i, j] = job.id

                    for j in range(ram_empty_index, job.ram_size + ram_empty_index):
                        cluster_ram_usage[i, j] = job.id

    RL_GLOBAL.fig, RL_GLOBAL.ax_list = plt.subplots(1, 2)

    RL_GLOBAL.ax_list[0].matshow(cluster_cpu_usage, cmap=plt.cm.tab20c)
    RL_GLOBAL.ax_list[0].set_title("CPU")
    RL_GLOBAL.ax_list[0].axis("off")
    for i in range(RL_GLOBAL.r + 1):
        for j in range(20 * RL_GLOBAL.t):
            c = cluster_cpu_usage[j, i]
            RL_GLOBAL.ax_list[0].text(i, j, str(c), va='center', ha='center')

    RL_GLOBAL.ax_list[1].matshow(cluster_ram_usage, cmap=plt.cm.tab20c)
    RL_GLOBAL.ax_list[1].set_title("RAM")
    RL_GLOBAL.ax_list[1].axis("off")
    for i in range(RL_GLOBAL.r + 1):
        for j in range(20 * RL_GLOBAL.t):
            c = cluster_ram_usage[j, i]
            RL_GLOBAL.ax_list[1].text(i, j, str(c), va='center', ha='center')

    RL_GLOBAL.fig.suptitle("t = 0", fontsize=16)

    plt.ion()
    plt.show()
    plt.pause(.2)
    time.sleep(.2)


def update_cluster_grid(t, jobs_scheduled):

    cluster_cpu_usage = np.zeros((20 * RL_GLOBAL.t, RL_GLOBAL.r + 1), dtype=int)
    cluster_ram_usage = np.zeros((20 * RL_GLOBAL.t, RL_GLOBAL.r + 1), dtype=int)

    if t >= 20 * RL_GLOBAL.t / 2:
        min_t = int(t - (20 * RL_GLOBAL.t / 2) + 1)
        max_t = int(t + (20 * RL_GLOBAL.t / 2))

        cluster_cpu_usage[:, 0] = [i for i in range(min_t, max_t + 1)]
        cluster_ram_usage[:, 0] = [i for i in range(min_t, max_t + 1)]

        temp_t = min_t

        for i in range(0, 20 * RL_GLOBAL.t):
            if len(jobs_scheduled) > 0:
                for job in jobs_scheduled:
                    if job.start <= temp_t <= job.finish:
                        cpu_empty_index = 1
                        ram_empty_index = 1

                        while cluster_cpu_usage[i, cpu_empty_index] != 0:
                            cpu_empty_index = cpu_empty_index + 1

                        while cluster_ram_usage[i, ram_empty_index] != 0:
                            ram_empty_index = ram_empty_index + 1

                        for j in range(cpu_empty_index, job.cpu_units + cpu_empty_index):
                            cluster_cpu_usage[i, j] = job.id

                        for j in range(ram_empty_index, job.ram_size + ram_empty_index):
                            cluster_ram_usage[i, j] = job.id
            temp_t = temp_t + 1

    else:
        cluster_cpu_usage[:, 0] = [i for i in range(20 * RL_GLOBAL.t)]
        cluster_ram_usage[:, 0] = [i for i in range(20 * RL_GLOBAL.t)]

        for i in range(0, 20 * RL_GLOBAL.t):
            if len(jobs_scheduled) > 0:
                for job in jobs_scheduled:
                    if job.start <= i <= job.finish:
                        cpu_empty_index = 1
                        ram_empty_index = 1

                        while cluster_cpu_usage[i, cpu_empty_index] != 0:
                            cpu_empty_index = cpu_empty_index + 1

                        while cluster_ram_usage[i, ram_empty_index] != 0:
                            ram_empty_index = ram_empty_index + 1

                        for j in range(cpu_empty_index, job.cpu_units + cpu_empty_index):
                            cluster_cpu_usage[i, j] = job.id

                        for j in range(ram_empty_index, job.ram_size + ram_empty_index):
                            cluster_ram_usage[i, j] = job.id

    RL_GLOBAL.ax_list[0].cla()
    RL_GLOBAL.ax_list[1].cla()

    RL_GLOBAL.ax_list[0].matshow(cluster_cpu_usage, cmap=plt.cm.tab20c)
    RL_GLOBAL.ax_list[0].set_title("CPU")
    for i in range(RL_GLOBAL.r + 1):
        for j in range(20 * RL_GLOBAL.t):
            c = cluster_cpu_usage[j, i]
            RL_GLOBAL.ax_list[0].text(i, j, str(c), va='center', ha='center')

    RL_GLOBAL.ax_list[1].matshow(cluster_ram_usage, cmap=plt.cm.tab20c)
    RL_GLOBAL.ax_list[1].set_title("RAM")
    for i in range(RL_GLOBAL.r + 1):
        for j in range(20 * RL_GLOBAL.t):
            c = cluster_ram_usage[j, i]
            RL_GLOBAL.ax_list[1].text(i, j, str(c), va='center', ha='center')

    RL_GLOBAL.fig.suptitle("t = " + str(t), fontsize=16)

    plt.draw()
    plt.pause(.2)
    plt.show()

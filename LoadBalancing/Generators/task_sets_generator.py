import random
import fastrand
import numpy as np

from Models.task import *


def create_task_set(params):
    task_id = 1
    task_set = []

    tasks_arrival_rate = np.random.randint(int(params["arrival_rate_per_10_time_units"]["min"]),
                                          int(params["arrival_rate_per_10_time_units"]["max"]))

    for i in range(int(int(params["data_set_length"]) / 10)):
        for j in range(tasks_arrival_rate):
            arrival = np.random.randint(i * 10, high=i*10+9)
            task = create_random_task(params)
            task['arrival'] = arrival
            task['id'] = task_id
            task_id = task_id + 1

            task_set.append(task)

    task_set.sort(key=lambda x: x['arrival'])

    return task_set


def create_random_task(params):
    execution = 0
    cpu_units = 0
    ram_size = 0

    r = int(params["r"])
    t = int(params["t"])

    tasks_length = params["tasks_length_by_t"]
    resources = params["resources_by_r"]

    task_type = np.random.choice(a=['short', 'medium', 'long'],
                                 p=[float(params["tasks_length_probabilities"]["short"]),
                                    float(params["tasks_length_probabilities"]["medium"]),
                                    float(params["tasks_length_probabilities"]["long"])])
    dominant_resource = np.random.choice(a=['cpu', 'ram'],
                                         p=[float(params["resources_probabilities"]["cpu"]),
                                            float(params["resources_probabilities"]["ram"])])

    # Compute execution time
    if task_type == 'short':
        execution = np.random.randint(int(tasks_length["short"]["min"]) * t,
                                      high=int(tasks_length["short"]["max"]) * t)
    elif task_type == 'medium':
        execution = np.random.randint(int(tasks_length["medium"]["min"]) * t,
                                      high=int(tasks_length["medium"]["max"]) * t)
    elif task_type == 'long':
        execution = np.random.randint(int(tasks_length["long"]["min"]) * t,
                                      high=int(tasks_length["long"]["max"]) * t)

    # Compute resources
    if dominant_resource == 'cpu':
        cpu_units = np.random.randint(int(float(resources["cpu"]["primary"]["min"]) * r),
                                      high=int(float(resources["cpu"]["primary"]["max"]) * r))
        ram_size = np.random.randint(int(float(resources["ram"]["secondary"]["min"]) * r),
                                     high=int(float(resources["ram"]["secondary"]["max"]) * r))
    elif dominant_resource == 'ram':
        cpu_units = np.random.randint(int(float(resources["cpu"]["secondary"]["min"]) * r),
                                      high=int(float(resources["cpu"]["secondary"]["max"]) * r))
        ram_size = np.random.randint(int(float(resources["ram"]["primary"]["min"]) * r),
                                     high=int(float(resources["ram"]["primary"]["max"]) * r))

    # Assign minimum resources if equals to zero
    if cpu_units == 0:
        cpu_units = 1
    if ram_size == 0:
        ram_size = 1

    task = Task(0, 0, execution, 0, cpu_units, ram_size, 0, 0, 0)

    return task

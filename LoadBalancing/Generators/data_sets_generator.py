from Generators.task_sets_generator import *

import numpy as np


def create_data_set(params):
    data_set = []

    for i in range(int(params["number_of_task_sets"])):
        task_set = create_task_set(params)
        data_set.append(task_set)

    return data_set

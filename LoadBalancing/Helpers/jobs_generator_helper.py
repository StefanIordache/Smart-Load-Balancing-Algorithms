import datetime
import random
import json
import os
from pathlib import Path
from operator import attrgetter
import time
from collections import *
import rapidjson

from Models.job import *
from Helpers.simulation_helper import *
from Helpers.io_helper import *
from Helpers.random_helper import *
from Helpers.global_helper import *

sum = 0


def generate_jobs(json_jobs):
    loaded_json = json.loads(json_jobs)

    if loaded_json['scenario'] == 'random':
        random_scenario(loaded_json['parameters'])
        return loaded_json['parameters']
    else:
        print('Invalid scenario')


def random_scenario(params):
    global sum

    jobs_path = GLOBAL.storage_path + "/Jobs"
    create_directory(jobs_path)

    GLOBAL.simulation_time = int(params['timeline']['generation_time'])

    GLOBAL.compute_batch_size_in_seconds(GLOBAL.simulation_time)

    number_of_batches = int(GLOBAL.simulation_time / GLOBAL.batch_size_in_seconds)

    for batch in range(number_of_batches):
        batch_storage_path = jobs_path + "/" + str(batch) + ".json"
        create_file(batch_storage_path)

        batch_content = []

        if GLOBAL.batch_size_in_seconds == 10:
            batch_content = generate_10_seconds_batch(batch, params)
        elif GLOBAL.batch_size_in_seconds == 100:
            batch_content = generate_100_seconds_batch(batch, params)


        batch_content = sort_by_arrival_time(batch_content)

        a = time.time()

        with open(batch_storage_path, 'w') as outfile:
            rapidjson.dump(batch_content, outfile, indent=4)

        b = time.time()
        sum = sum + (b - a)

    if number_of_batches * GLOBAL.batch_size_in_seconds < GLOBAL.simulation_time:
        batch_storage_path = jobs_path + "/" + str(number_of_batches) + ".json"
        create_file(batch_storage_path)

        batch_content = []

        for sec in range(number_of_batches * GLOBAL.batch_size_in_seconds, GLOBAL.simulation_time):
            batch_content.extend(generate_1_second_batch(sec, params))

        batch_content = sort_by_arrival_time(batch_content)

        with open(batch_storage_path, 'w') as outfile:
            rapidjson.dump(batch_content, outfile, indent=4)

        number_of_batches = number_of_batches + 1

    GLOBAL.number_of_batches = number_of_batches


def generate_100_seconds_batch(batch_index, params):

    batch_content = []

    for sec in range(10):
        batch_content.extend(generate_10_seconds_batch(batch_index * 10 + sec, params))

    return batch_content


def generate_10_seconds_batch(batch_index, params):

    batch_content = []

    for sec in range(10):
        batch_content.extend(generate_1_second_batch(batch_index * 10 + sec, params))

    return batch_content


def generate_1_second_batch(second, params):

    batch_content = []

    distribution = int(params['timeline']['distribution'])

    for job in range(distribution):
        batch_content.append(random_job(second, params))

    return batch_content


def sort_by_arrival_time(batch):

    batch.sort(key=lambda x: x.arrival, reverse=False)

    return batch

import datetime
import random
import json
import os
from pathlib import Path

from Models.job import *
from Helpers.simulation_helper import *
from Helpers.io_helper import *
from Helpers.random_helper import *
from Helpers.global_helper import *



def generate_jobs(json_jobs):
    loaded_json = json.loads(json_jobs)

    print(loaded_json)

    if loaded_json['scenario'] == 'random':
        number_of_batches, temp_location = random_scenario(loaded_json['parameters'])
        return number_of_batches, temp_location, loaded_json['parameters']
    else:
        print('Invalid scenario')


def random_scenario(params):
    base_path = str(Path(os.path.dirname(__file__)).parent)

    create_directory(base_path + "/Temp")
    create_directory(base_path + "/Temp/Jobs")

    temp_location = str(Path(os.path.dirname(__file__)).parent) + "/Temp/Jobs/"
    temp_location = temp_location + str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))

    create_directory(temp_location)

    GLOBAL.simulation_time = int(params['timeline']['generation_time'])

    GLOBAL.compute_batch_size_in_seconds(GLOBAL.simulation_time)

    number_of_batches = int(GLOBAL.simulation_time / GLOBAL.batch_size_in_seconds)

    for batch in range(number_of_batches):
        batch_storage_path = temp_location + "/" + str(batch) + ".json"
        create_file(batch_storage_path)

        if GLOBAL.batch_size_in_seconds == 10:
            batch_content = generate_10_seconds_batch(batch, params)
        elif GLOBAL.batch_size_in_seconds == 100:
            batch_content = generate_100_seconds_batch(batch, params)

        with open(batch_storage_path, 'w') as outfile:
            json.dump(batch_content, outfile, indent=4)

    if number_of_batches * GLOBAL.batch_size_in_seconds < GLOBAL.simulation_time:
        batch_storage_path = temp_location + "/" + str(number_of_batches) + ".json"
        create_file(batch_storage_path)

        batch_content = []

        for sec in range(number_of_batches * GLOBAL.batch_size_in_seconds, GLOBAL.simulation_time):
            batch_content.extend(generate_1_second_batch(sec, params))

        with open(batch_storage_path, 'w') as outfile:
            json.dump(batch_content, outfile, indent=4)

        number_of_batches = number_of_batches + 1

    return number_of_batches, temp_location


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

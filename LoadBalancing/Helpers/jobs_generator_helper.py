import datetime
import random
import json
import os
from pathlib import Path

from Models.job import *
from Helpers.io_helper import *
from Helpers.random_helper import *


def generate_jobs(json_jobs):
    loaded_json = json.loads(json_jobs)

    print(loaded_json)

    if loaded_json['scenario'] == 'random':
        return random_scenario(loaded_json['parameters'])
    else:
        print('Invalid scenario')


def random_scenario(params):
    base_path = str(Path(os.path.dirname(__file__)).parent)

    create_directory(base_path + "/Temp")
    create_directory(base_path + "/Temp/Jobs")

    temp_location = str(Path(os.path.dirname(__file__)).parent) + "/Temp/Jobs/"
    temp_location = temp_location + str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))

    create_directory(temp_location)

    generation_time = int(params['timeline']['generation_time'])

    batches = int(generation_time / 10)

    for batch in range(batches):
        batch_storage_path = temp_location + "/" + str(batch * 10) + "-" + str((batch + 1) * 10) + ".json"
        create_file(batch_storage_path)

        batch_content = generate_10_seconds_batch(batch, params)

        with open(batch_storage_path, 'w') as outfile:
            json.dump(batch_content, outfile, indent=4)

    if batches * 10 < generation_time:
        batch_storage_path = temp_location + "/" + str(batches * 10) + "-" + str(generation_time) + ".json"
        create_file(batch_storage_path)

        batch_content = []

        for sec in range(batches * 10, generation_time):
            batch_content.extend(generate_1_second_batch(sec, params))

        with open(batch_storage_path, 'w') as outfile:
            json.dump(batch_content, outfile, indent=4)

        batches = batches + 1

    return batches, temp_location


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

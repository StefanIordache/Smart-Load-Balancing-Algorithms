import datetime
import random
import json
import os
from pathlib import Path

from Models.job import *
from Helpers.io_helper import *


def generate_jobs(json_jobs):
    loaded_json = json.loads(json_jobs)

    print(loaded_json)

    if loaded_json['scenario'] == 'random':
        random_scenario(loaded_json['parameters'])
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
        batch_storage_path = temp_location + "/" + str(batch * 10) + "-" + str((batch + 1) * 10), ".json"
        create_file(batch_storage_path)

        batch_content = generate_10_sec_batch(batch, params['parameters'])

    if batches * 10 < generation_time:
        f = open(temp_location + "/" + str(batches * 10) + "-" + str(generation_time) + ".json", "w+")
        f.close()
        batches = batches + 1

    return batches


def generate_10_sec_batch(batch_index, params):
    return 1


def generate_1_sec_batch(index, params):
    return 1
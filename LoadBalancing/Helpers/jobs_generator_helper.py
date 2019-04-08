import datetime
import json
import os
from pathlib import Path

from Models.job import *


def generate_jobs(json_jobs):
    loaded_json = json.loads(json_jobs)

    print(loaded_json)

    if loaded_json['scenario'] == 'random':
        random_scenario(loaded_json['parameters'])
    else:
        print('Invalid scenario')


def random_scenario(params):

    print(params.keys())

    os.path.dirname(__file__)
    temp_location = str(Path(os.path.dirname(__file__)).parent) + "/Temp/Jobs/"
    temp_location = temp_location + str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))

    generation_time = int(params['timeline']['generation_time'])

    batches = int(generation_time / 10)

    os.mkdir(temp_location)

    for batch in range(batches):
        f = open(temp_location + "/" + str(batch * 10) + "-" + str((batch + 1) * 10) + ".txt", "w+")
        f.close()

    if batches * 10 < generation_time:
        f = open(temp_location + "/" + str(batches * 10) + "-" + str(generation_time) + ".txt", "w+")
        f.close()

    batches = batches + 1

    print(temp_location)

    return batches

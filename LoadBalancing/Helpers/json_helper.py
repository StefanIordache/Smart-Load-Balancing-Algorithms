import json
from collections import namedtuple

from Models.system import *


def unpack_cluster(json_cluster):
    loaded_json = json.loads(json_cluster)

    systems = []

    for item in loaded_json["systems"]:
        system = namedtuple("System", item.keys())(*item.values())
        systems.append(system)

    return systems


def load_jobs_batch(file_location):
    batch = []

    with open(file_location) as json_file:
        data = json.load(json_file)

        for item in data:
            job = namedtuple("Job", item.keys())(*item.values())
            batch.append(job)

    return batch


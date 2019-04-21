import json
from sortedcontainers import *
from collections import namedtuple
import time
import gc
from collections import deque
import rapidjson

from Helpers.global_helper import *

from Models.system import *
from Models.job import *


def unpack_cluster(json_cluster):
    loaded_json = json.loads(json_cluster)

    systems = []

    for item in loaded_json["systems"]:
        system = namedtuple("System", item.keys())(*item.values())
        systems.append(system)

    return systems


def load_jobs_batch(file_location):

    batch = deque()

    # gc.disable()

    with open(file_location) as json_file:
        data = json.load(json_file)

        # Faster, but not enough
        # batch = deque([namedtuple("Job", item.keys())(*item.values()) for item in data])
        for item in data:

            # Explicit is faster than "namedtuple"
            job = Job(item['arrival'], item['execution'], item['deadline'],
                      item['cpu_units'], item['priority'], item['profit'])

            # Slow version
            # job = namedtuple("Job", item.keys())(*item.values())
            batch.append(job)

    # gc.enable()

    return batch


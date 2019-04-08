import json
from collections import namedtuple

from Models.system import *


def unpack_cluster_json(json_cluster):
    loaded_json = json.loads(json_cluster)

    systems = []

    for item in loaded_json["systems"]:
        system = namedtuple("System", item.keys())(*item.values())
        systems.append(system)

    return systems

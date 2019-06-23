import os
import sys
import rapidjson
import json
from pathlib import Path

from Models.task import *


def create_directory(path):

    try:
        os.mkdir(path, mode=0o777)
    except FileExistsError:
        print("File/Folder Exists - " + path)

    return path


def create_file(path, extension=""):
    f = open(path + extension, "w+")
    f.close()

    return path


def append_to_file(path, info):
    try:
        with open(path, "a") as file:
            file.write(info)
    except Exception as e:
        print("Append Error:\n" + str(e))
    return path


def write_to_file(path, info):
    try:
        with open(path, "w+") as file:
            file.write(info)
    except Exception as e:
        print("Append Error:\n" + str(e))
    return path


def write_data_set(data_set_storage_path, data_set):

    print(len(data_set))

    for i in range(len(data_set)):
        task_set_path = data_set_storage_path + "/" + str(i) + ".json"
        create_file(task_set_path)

        task_set = data_set[i]
        write_task_set(task_set_path, task_set)


def read_data_set(data_set_id):
    data_set_path = str(Path(os.path.dirname(__file__)).parent) + "TestEnvironment/app/storage/data_sets/" + str(data_set_id)

    data_set = []

    try:
        task_sets_names = [f for f in os.listdir(data_set_path) if os.path.isfile(os.path.join(data_set_path, f))]
        task_sets_names.sort()

        for task_set_name in task_sets_names:
            task_set = read_task_set(data_set_path + "/" + task_set_name)
            data_set.append(task_set)
    except FileNotFoundError:
        return []

    return data_set


def write_task_set(task_set_path, task_set):
    with open(task_set_path, 'w') as outfile:
        rapidjson.dump(task_set, outfile, indent=4)


def read_task_set(task_set_path):
    task_set = []

    with open(task_set_path) as infile:
        data = json.load(infile)

        for item in data:
            task = Task(item['id'], item['arrival'], item['execution'], item['deadline'],
                        item['cpu_units'], item['ram_size'], item['disk_size'], item['profit'])

            task_set.append(task)

    return task_set

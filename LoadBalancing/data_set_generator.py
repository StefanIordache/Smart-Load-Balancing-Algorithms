import sys
import time
import json
import socket
import datetime
import time
import random

from pathlib import Path
from Helpers.io_helper import *

from Generators.data_sets_generator import *


def create_storage_path(data_set_directory):
    base_path = str(Path(os.path.dirname(__file__)).parent)

    storage_path = create_directory(base_path + "/TestEnvironment/app/storage")
    storage_path = create_directory(storage_path + "/data_sets")
    storage_directory = str(data_set_directory)
    storage_path = create_directory(storage_path + '/' + storage_directory)

    return storage_path


if __name__ == "__main__":

    # random.seed(672367)

    start = time.time()

    host = ''
    port = 3001

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    connected = False

    while not connected:
        try:
            sock.connect((host, port))
            connected = True
        except Exception as e:
            time.sleep(0.3)
            pass

    connection_time = time.time()
    print("Connection time: " + str(connection_time - start))

    while True:

        data_set_id = int(sock.recv(1024).decode())
        print(data_set_id)

        data_set_json = sock.recv(1024).decode()
        print(data_set_json)

        data_set_storage_path = create_storage_path(str(data_set_id))

        data_set = create_data_set(json.loads(data_set_json))

        write_data_set(data_set_storage_path, data_set)

        time.sleep(0.1)
        sock.sendall("FINISHED".encode())
        time.sleep(0.1)
        sock.sendall("NO ERRORS".encode())
        time.sleep(0.1)
        sock.sendall(str(data_set_id).encode())

        break

    sock.close()

    end = time.time()
    print("Data Set generation time: " + str(end - connection_time))


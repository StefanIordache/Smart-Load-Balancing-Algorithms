import sys
import time
import json
import socket
import datetime
import time
import random

from Models.system import *
from Helpers.json_helper import *
from Helpers.jobs_generator_helper import *
from Helpers.simulation_helper import *
from Helpers.global_helper import *


def set_algorithm(algorithm):
    if algorithm == 'FCFS':
        GLOBAL.algorithm = Algorithm.FCFS
    elif algorithm == 'PARALLELIZED-FCFS':
        GLOBAL.algorithm = Algorithm.PARALLELIZED_FCFS
    elif algorithm == 'OPTIMIZED-FCFS':
        GLOBAL.algorithm = Algorithm.OPTIMIZED_FCFS
    elif algorithm == 'MCT':
        GLOBAL.algorithm = Algorithm.MCT
    elif algorithm == 'SJF':
        GLOBAL.algorithm = Algorithm.SJF
    else:
        GLOBAL.algorithm = Algorithm.BLANK


if __name__ == "__main__":

    random.seed(672367)

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

        simulation_id = int(sock.recv(1024).decode())
        GLOBAL.simulation_id = simulation_id

        json_cluster = sock.recv(1024).decode()

        systems = unpack_cluster(json_cluster)

        json_simulation = sock.recv(1024).decode()

        simulated_algorithm = sock.recv(1024).decode()
        simulated_algorithm = simulated_algorithm.rstrip()

        set_algorithm(simulated_algorithm)

        data_set_id = int(sock.recv(1024).decode())

        # start_simulation(systems, simulation_params)

        time.sleep(0.1)
        sock.sendall("FINISHED".encode())
        time.sleep(0.1)
        sock.sendall("NO ERRORS".encode())
        time.sleep(0.1)
        sock.sendall(GLOBAL.storage_directory.encode())

        break

    sock.close()

    end = time.time()
    print("Simulation time: " + str(end - connection_time))


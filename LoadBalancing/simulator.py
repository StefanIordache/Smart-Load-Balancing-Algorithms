import sys
import time
import json
import socket
import datetime
import time
import random

from Models.cluster import *
from Models.simulation import *
from Helpers.simulation_helper import *
from Helpers.global_helper import *
from Helpers.io_helper import *


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

        print(simulation_id)

        cluster_info = sock.recv(1024).decode()

        cluster = Cluster.unpack_cluster(cluster_info)

        print(cluster)

        simulation_info = sock.recv(1024).decode()

        simulation = Simulation.unpack_simulation_info(simulation_info)

        print(simulation)

        simulated_algorithm = sock.recv(1024).decode()
        simulated_algorithm = simulated_algorithm.rstrip()

        print(simulated_algorithm)

        set_algorithm(simulated_algorithm)

        data_set_id = int(sock.recv(1024).decode())
        data_set = read_data_set(data_set_id)

        print(len(data_set))

        start_simulation(cluster, simulation, data_set)

        time.sleep(0.1)
        sock.sendall("FINISHED".encode())
        time.sleep(0.1)
        sock.sendall("NO ERRORS".encode())

        break

    sock.close()

    end = time.time()
    print("Simulation time: " + str(end - connection_time))


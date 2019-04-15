import sys
import time
import json
import socket

from Models.system import *
from Helpers.json_helper import *
from Helpers.jobs_generator_helper import *
from Helpers.simulation_helper import *
from Helpers.global_helper import *


if __name__ == "__main__":

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

    while True:
        json_cluster = sock.recv(1024).decode()

        systems = unpack_cluster(json_cluster)

        sock.sendall("OK_CLUSTER".encode())

        json_jobs = sock.recv(1024).decode()

        number_of_batches, temp_location, simulation_params = generate_jobs(json_jobs)

        sock.sendall("OK_JOBS".encode())

        simulated_algorithm = sock.recv(1024).decode()
        simulated_algorithm = simulated_algorithm.rstrip()

        sock.sendall("OK_ALGORITHM".encode())

        start_simulation(simulated_algorithm, systems, temp_location, number_of_batches, simulation_params)

        sock.sendall("FINISHED".encode())
        sock.sendall("NO ERRORS".encode())

        print("finished")

        break

    sock.close()

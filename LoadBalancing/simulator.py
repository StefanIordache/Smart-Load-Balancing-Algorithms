import sys
import time
import json
import socket

from Models.system import*
from Helpers.json_helper import*


if __name__ == "__main__":

    # info_cluster = sys.stdin.readline()
    # json_cluster = str(info_cluster)
    #
    # print("OK1")
    # sys.stdout.flush()
    #
    # info_jobs = sys.stdin.readline()
    # jobs = str(info_jobs)
    #
    # print("OK2")
    # sys.stdout.flush()
    #
    # json_cluster = '{"number_of_systems":3,"systems":[{"name":"sys-1","cpu_cores":8,"cpu_units":100,"ram_size":8192,"disk_size":5120,"mips":20},{"name":"sys-2","cpu_cores":4,"cpu_units":100,"ram_size":16384,"disk_size":5120,"mips":15},{"name":"sys-3","cpu_cores":10,"cpu_units":100,"ram_size":4096,"disk_size":8192,"mips":40}]}'
    # json_jobs = '{"scenario":"random","parameters":{"usage":{"min_cpu_units":20,"max_cpu_units":30},"timeline":{"distribution":10,"generation_time":200},"priority":{"type":"constant","value":1}}}'
    #
    # systems = unpack_cluster_json(json_cluster)
    # print(systems)

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

        print(json_cluster)

        systems = unpack_cluster_json(json_cluster)
        print(systems)

        sock.sendall("OK1".encode())

        json_jobs = sock.recv(1024).decode()

        print(json_jobs)

        sock.sendall("OK2".encode())

        break

    sock.close()

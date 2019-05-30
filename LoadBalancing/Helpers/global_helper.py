from Models.algorithm import *
import time


class Globals:

    __instance = None

    simulation_id = -1

    time_precision = 0.01
    time_precision_factor = 100
    batch_size_in_seconds = 10
    simulation_time = 0
    number_of_batches = 0
    storage_path = ""
    storage_directory = ""
    algorithm = Algorithm.BLANK

    time_start = time.time()
    time_jobs_generation = time.time()
    time_simulation = time.time()
    time_end = time.time()

    cluster = []
    current_cluster_state = []

    profit = 0

    @staticmethod
    def getInstance():
        if Globals.__instance == None:
            Globals()
        return Globals.__instance

    def __init__(self):
        if Globals.__instance != None:
            raise Exception("Globals is a singleton class!")
        else:
            self.simulation_id = -1
            self.time_precision = 0.01
            self.time_precision_factor = 100
            self.batch_size_in_seconds = 10
            self.simulation_time = 0
            self.number_of_batches = 0
            self.storage_path = ""
            self.storage_directory = ""
            self.algorithm = Algorithm.BLANK
            self.cluster = []
            self.current_cluster_state = []
            Globals.__instance = self

    def compute_batch_size_in_seconds(self, simulation_time):
        if simulation_time < 10000:
            self.batch_size_in_seconds = 10
        elif 10000 <= simulation_time < 100000:
            self.batch_size_in_seconds = 100
        elif simulation_time >= 100000:
            self.batch_size_in_seconds = 1000


GLOBAL = Globals()

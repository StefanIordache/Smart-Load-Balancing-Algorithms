from Models.algorithm import *
import time


class Globals:

    __instance = None

    simulation_id = 0
    data_set_id = 0
    algorithm = None

    r = 0
    t = 0
    allocation_subset_size = 10

    fig = None
    ax_list = None

    @staticmethod
    def get_instance():
        if Globals.__instance is None:
            Globals()
        return Globals.__instance

    def __init__(self):
        if Globals.__instance is not None:
            raise Exception("Globals is a singleton class!")
        else:
            self.simulation_id = 0
            self.data_set_id = 0
            self.algorithm = None

            self.r = 0
            self.t = 0
            self.allocation_subset_size = 10

            self.fig = None
            self.ax_list = None
            Globals.__instance = self


GLOBAL = Globals()

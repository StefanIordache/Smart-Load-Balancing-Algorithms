class Globals:

    __instance = None
    time_precision = 0.01
    time_precision_factor = 100
    batch_size_in_seconds = 10
    simulation_time = 0

    @staticmethod
    def getInstance():
        if Globals.__instance == None:
            Globals()
        return Globals.__instance

    def __init__(self):
        if Globals.__instance != None:
            raise Exception("Globals is a singleton class!")
        else:
            self.time_precision = 0.01
            self.time_precision_factor = 100
            self.batch_size_in_seconds = 10
            self.simulation_time = 0
            Globals.__instance = self

    def compute_batch_size_in_seconds(self, simulation_time):
        if simulation_time < 10000:
            self.batch_size_in_seconds = 10
        elif 10000 <= simulation_time < 100000:
            self.batch_size_in_seconds = 100
        elif simulation_time >= 100000:
            self.batch_size_in_seconds = 1000


GLOBAL = Globals()

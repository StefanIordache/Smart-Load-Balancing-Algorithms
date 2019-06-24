import json


class Simulation(dict):

    def __init__(self, t=0, frame_size=0, length=0, allocation_subset_size=0):
        dict.__init__(self,
                      t=t,
                      frame_size=frame_size,
                      length=length,
                      allocation_subset_size=allocation_subset_size)
        self.t = t
        self.frame_size = frame_size
        self.length = length
        self.allocation_subset_size = allocation_subset_size

    @staticmethod
    def unpack_simulation_info(simulation_info):
        data = json.loads(simulation_info)

        t = int(data["t"])
        frame_size = int(data["frame_size"])
        simulation_length = int(data["simulation_length"])
        allocation_subset_size = int(data["allocation_subset_size"])

        simulation = Simulation(t, frame_size, simulation_length, allocation_subset_size)

        return simulation



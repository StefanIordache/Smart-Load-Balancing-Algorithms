class Job:

    def __init__(self, arrival, execution, cpu_units, priority):
        self.arrival = arrival
        self.execution = execution
        self.cpu_units = cpu_units
        self.priority = priority

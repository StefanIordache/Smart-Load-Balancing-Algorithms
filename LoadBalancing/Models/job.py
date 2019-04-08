class Job(dict):

    def __init__(self, arrival, execution, cpu_units, priority, profit):
        dict.__init__(self,
                      arrival=arrival,
                      execution=execution,
                      cpu_units=cpu_units,
                      priority=priority,
                      profit=profit)
        # self.arrival = arrival
        # self.execution = execution
        # self.cpu_units = cpu_units
        # self.priority = priority
        # self.profit = profit

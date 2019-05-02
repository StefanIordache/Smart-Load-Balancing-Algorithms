class Job(dict):

    def __init__(self, arrival=0, execution=0, deadline=0, cpu_units=0, priority=0, profit=0, finish=0, system_index=0):
        dict.__init__(self,
                      arrival=arrival,
                      execution=execution,
                      deadline=deadline,
                      cpu_units=cpu_units,
                      priority=priority,
                      profit=profit,
                      finish=finish,
                      system_index=system_index)
        self.arrival = arrival
        self.execution = execution
        self.deadline = deadline
        self.cpu_units = cpu_units
        self.priority = priority
        self.profit = profit
        self.finish = finish
        self.system_index = system_index

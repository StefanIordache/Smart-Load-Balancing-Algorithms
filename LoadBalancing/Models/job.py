class Job(dict):

    def __init__(self, arrival, execution, deadline, cpu_units, priority, profit):
        dict.__init__(self,
                      arrival=arrival,
                      execution=execution,
                      deadline=deadline,
                      cpu_units=cpu_units,
                      priority=priority,
                      profit=profit)

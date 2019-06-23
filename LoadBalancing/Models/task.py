class Task(dict):

    def __init__(self, id=0, arrival=0, execution=0, deadline=0,
                 cpu_units=0, ram_size=0, disk_size=0,
                 profit=0, finish=0, remaining=0, start=0):
        dict.__init__(self,
                      id=id,
                      arrival=arrival,
                      execution=execution,
                      deadline=deadline,
                      cpu_units=cpu_units,
                      ram_size=ram_size,
                      disk_size=disk_size,
                      profit=profit,
                      finish=finish,
                      remaining=remaining,
                      start=start)
        self.id = id
        self.arrival = arrival
        self.execution = execution
        self.deadline = deadline
        self.cpu_units = cpu_units
        self.ram_size = ram_size
        self.disk_size = disk_size
        self.profit = profit
        self.finish = finish
        self.remaining = remaining
        self.start = start

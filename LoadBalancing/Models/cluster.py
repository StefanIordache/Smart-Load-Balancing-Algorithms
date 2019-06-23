class Cluster(dict):

    def __init__(self, cpu_units=0, ram_size=0, disk_size=0):
        dict.__init__(self,
                      cpu_units=cpu_units,
                      ram_size=ram_size,
                      disk_size=disk_size)
        self.cpu_units = cpu_units
        self.ram_size = ram_size
        self.disk_size = disk_size



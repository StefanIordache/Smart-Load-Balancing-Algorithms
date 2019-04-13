class System(dict):

    def __init__(self, name, cpu_units, ram_size, disk_size):
        dict.__init__(self,
                      name=name,
                      cpu_units=cpu_units,
                      ram_size=ram_size,
                      disk_size=disk_size)

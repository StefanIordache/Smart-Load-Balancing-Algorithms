import json


class Cluster(dict):

    def __init__(self, r=0, cpu_units=0, ram_size=0, disk_size=0):
        dict.__init__(self,
                      r=r,
                      cpu_units=cpu_units,
                      ram_size=ram_size,
                      disk_size=disk_size)
        self.r = r
        self.cpu_units = cpu_units
        self.ram_size = ram_size
        self.disk_size = disk_size

    @staticmethod
    def unpack_cluster(cluster_info):
        data = json.loads(cluster_info)

        r = int(data["r"])
        cpu_ratio = int(data["resources_ratios"]["cpu"])
        ram_ratio = int(data["resources_ratios"]["ram"])

        cluster = Cluster(r, r * cpu_ratio, r * ram_ratio, 0)

        return cluster



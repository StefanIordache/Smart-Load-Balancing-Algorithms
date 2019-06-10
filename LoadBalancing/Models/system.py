class System(dict):

    def __init__(self, name="",
                 cpu_cores=0, cpu_units=0, cpu_units_per_second_per_core=0,
                 ram_size=0, disk_size=0,
                 does_have_gpu=False, gpu_vram_size=0, gpu_computational_cores=0,
                 cpu_cores_available_units=[]):
        dict.__init__(self,
                      name=name,
                      cpu_cores=cpu_cores,
                      cpu_units=cpu_units,
                      cpu_units_per_second_per_core=cpu_units_per_second_per_core,
                      ram_size=ram_size,
                      disk_size=disk_size,
                      does_have_gpu=does_have_gpu,
                      gpu_vram_size=gpu_vram_size,
                      gpu_computational_cores=gpu_computational_cores,
                      cpu_cores_available_units=cpu_cores_available_units)
        self.name = name
        self.cpu_cores = cpu_cores
        self.cpu_units = cpu_units
        self.cpu_units_per_second_per_core = cpu_units_per_second_per_core
        self.ram_size = ram_size
        self.disk_size = disk_size
        self.does_have_gpu = does_have_gpu
        self.gpu_vram_size = gpu_vram_size
        self.gpu_computational_cores = gpu_computational_cores
        self.cpu_cores_available_units = cpu_cores_available_units

class Job(dict):

    def __init__(self, arrival=0, execution=0, deadline=0, cpu_units=0, ram_size=0, disk_size=0, needs_gpu=False, gpu_vram_size=0, gpu_computational_cores=0, priority=0, profit=0, finish=0, system_index=0):
        dict.__init__(self,
                      arrival=arrival,
                      execution=execution,
                      deadline=deadline,
                      cpu_units=cpu_units,
                      ram_size=ram_size,
                      disk_size=disk_size,
                      needs_gpu=needs_gpu,
                      gpu_vram_size=gpu_vram_size,
                      gpu_computational_cores=gpu_computational_cores,
                      priority=priority,
                      profit=profit,
                      finish=finish,
                      system_index=system_index)
        self.arrival = arrival
        self.execution = execution
        self.deadline = deadline
        self.cpu_units = cpu_units
        self.ram_size = ram_size
        self.disk_size = disk_size
        self.needs_gpu = needs_gpu
        self.gpu_vram_size = gpu_vram_size
        self.gpu_computational_cores = gpu_computational_cores
        self.priority = priority
        self.profit = profit
        self.finish = finish
        self.system_index = system_index

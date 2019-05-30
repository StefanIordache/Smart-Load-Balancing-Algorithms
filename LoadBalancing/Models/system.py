class System(dict):

    def __init__(self, name="", cpu_units=0, ram_size=0, disk_size=0, does_have_gpu=False, gpu_vram_size=0, gpu_computational_cores=0):
        dict.__init__(self,
                      name=name,
                      cpu_units=cpu_units,
                      ram_size=ram_size,
                      disk_size=disk_size,
                      does_have_gpu=does_have_gpu,
                      gpu_vram_size=gpu_vram_size,
                      gpu_computational_cores=gpu_computational_cores)
        self.name = name
        self.cpu_units = cpu_units
        self.ram_size = ram_size
        self.disk_size = disk_size
        self.does_have_gpu = does_have_gpu
        self.gpu_vram_size = gpu_vram_size
        self.gpu_computational_cores = gpu_computational_cores

    '''
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def cpu_units(self):
        return self._cpu_units
    
    @cpu_units.setter
    def cpu_units(self, value):
        self._cpu_units = value

    @cpu_units.deleter
    def cpu_units(self):
        del self._cpu_units

    @property
    def ram_size(self):
        return self._ram_size

    @ram_size.setter
    def ram_size(self, value):
        self._ram_size = value

    @ram_size.deleter
    def ram_size(self):
        del self._ram_size

    @property
    def disk_size(self):
        return self._disk_size

    @disk_size.setter
    def disk_size(self, value):
        self._disk_size = value

    @disk_size.deleter
    def disk_size(self):
        del self._disk_size'''

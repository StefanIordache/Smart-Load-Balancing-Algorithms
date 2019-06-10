import random
import fastrand

from Models.job import *
from Models.system import *


def random_job(second, params):

    arrival = round(second + random.random(), 2)
    min_cpu_units = int(params['usage']['min_cpu_units'])
    max_cpu_units = int(params['usage']['max_cpu_units'])
    min_ram_size = int(params['usage']['min_ram_size'])
    max_ram_size = int(params['usage']['max_ram_size'])
    min_disk_size = int(params['usage']['min_disk_size'])
    max_disk_size = int(params['usage']['max_disk_size'])
    min_deadline = float(params['deadline']['min'])
    max_deadline = float(params['deadline']['max'])
    min_priority = int(params['priority']['min'])
    max_priority = int(params['priority']['max'])
    min_profit = float(params['profit']['min'])
    max_profit = float(params['profit']['max'])

    # CPU parallel processing

    can_be_parallelized_on_cpu = False
    max_cpu_cores = 1

    parallelization_probability = int(params['usage']['parallel_cpu_processing']['probability'])
    random_parallelization_probability = 1 + fastrand.pcg32bounded(100)

    if random_parallelization_probability <= parallelization_probability:
        can_be_parallelized_on_cpu = True
        max_cpu_cores = 2 + fastrand.pcg32bounded(int(params['usage']['parallel_cpu_processing']['max_cpu_cores']) - 1)

    gpu_vram_size = 0
    gpu_computational_cores = 0
    needs_gpu = False

    # GPU processing

    min_gpu_vram_size = int(params['usage']['gpu']['min_vram_size'])
    max_gpu_vram_size = int(params['usage']['gpu']['max_vram_size'])
    min_gpu_computational_cores = int(params['usage']['gpu']['min_computational_cores'])
    max_gpu_computational_cores = int(params['usage']['gpu']['max_computational_cores'])

    needs_gpu_probability = int(params['usage']['gpu']['probability'])
    random_gpu_probability = 1 + fastrand.pcg32bounded(100)

    if random_gpu_probability <= needs_gpu_probability:
        needs_gpu = True
        gpu_vram_size = min_gpu_vram_size + fastrand.pcg32bounded(max_gpu_vram_size - min_gpu_vram_size + 1)
        gpu_computational_cores = min_gpu_computational_cores + \
                                  fastrand.pcg32bounded(max_gpu_computational_cores - min_gpu_computational_cores + 1)

    deadline = round(random.uniform(min_deadline, max_deadline), 2)
    cpu_units = min_cpu_units + fastrand.pcg32bounded(max_cpu_units - min_cpu_units + 1)
    ram_size = min_ram_size + fastrand.pcg32bounded(max_ram_size - min_ram_size + 1)
    disk_size = min_disk_size + fastrand.pcg32bounded(max_disk_size - min_disk_size + 1)
    priority = min_priority + fastrand.pcg32bounded(max_priority - min_priority + 1)
    profit = round(random.uniform(min_profit, max_profit), 2)

    job = Job(arrival, 0, deadline, cpu_units, ram_size, disk_size,
              can_be_parallelized_on_cpu, max_cpu_cores,
              needs_gpu, gpu_vram_size, gpu_computational_cores,
              priority, profit)

    return job

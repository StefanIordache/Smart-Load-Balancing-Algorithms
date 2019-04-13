import random

from Models.job import *
from Models.system import *


def random_job(second, params):
    job = Job(second + round(random.random(), 2),
              round(random.uniform(float(params['execution']['min']),
                                   float(params['execution']['max'])),
                    2),
              round(random.uniform(float(params['deadline']['min']),
                                   float(params['deadline']['max'])),
                    2),
              random.randint(int(params['usage']['min_cpu_units']),
                             int(params['usage']['max_cpu_units'])),
              random.randint(int(params['priority']['min']),
                             int(params['priority']['max'])),
              round(random.uniform(float(params['profit']['min']),
                                   float(params['profit']['max'])),
                    2),
              )

    return job

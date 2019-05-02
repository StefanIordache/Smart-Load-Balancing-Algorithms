import random
import fastrand

from Models.job import *
from Models.system import *


def random_job(second, params):

    arrival = round(second + random.random(), 2)
    min_cpu_units = int(params['usage']['min_cpu_units'])
    max_cpu_units = int(params['usage']['max_cpu_units'])
    min_execution = float(params['execution']['min'])
    max_execution = float(params['execution']['max'])
    min_deadline = float(params['deadline']['min'])
    max_deadline = float(params['deadline']['max'])
    min_priority = int(params['priority']['min'])
    max_priority = int(params['priority']['max'])
    min_profit = float(params['profit']['min'])
    max_profit = float(params['profit']['max'])

    execution = round(random.uniform(min_execution, max_execution), 2)
    deadline = round(random.uniform(max(min_deadline, execution), max_deadline), 2)
    cpu_units = min_cpu_units + fastrand.pcg32bounded(max_cpu_units - min_cpu_units + 1)
    priority = min_priority + fastrand.pcg32bounded(max_priority - min_priority + 1)
    profit = round(random.uniform(min_profit, max_profit), 2)

    job = Job(arrival, execution, deadline, cpu_units, priority, profit)

    return job

from Algorithms.FCSF import *


def start_simulation(selected_algorithm, systems, jobs_location, number_of_batches, params):

    if selected_algorithm == "FCFS":
        run_FCFS(systems, jobs_location, number_of_batches, params)

    return 1

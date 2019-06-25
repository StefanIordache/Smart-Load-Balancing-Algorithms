import numpy as np
import math

import task_distribution


class Parameters:
    def __init__(self):

        self.output_filename = 'data/tmp'

        self.num_epochs = 1000         # (Number of training epochs)
        self.simu_len = 50             # (Cycle length)
        self.num_ex = 10              # (Number of task sets)

        self.output_freq = 10          # (Output + Storage interval)

        self.num_seq_per_batch = 10    # (Number of task sets in order to compute baseline)
        self.episode_max_length = 200  # (Maximum episode length)

        self.num_res = 2               # (Number of resources)
        self.num_nw = 5                # (Maximum number of tasks in queue)

        self.time_horizon = 20         # (Time steps in the graph)
        self.max_job_len = 15          # (Maximum job length for training)
        self.res_slot = 10             # (Maximum available resource slots)
        self.max_job_size = 10         # (Maximum resource request per task)

        self.backlog_size = 60         # (Backlog queue size)

        self.max_track_since_new = 10  # (Track maximum time steps since last new task)

        self.job_num_cap = 40          # (Maximum distinct colors in graph)

        self.new_job_rate = 0.7        # (Lambda for arrival Poisson Process)

        self.discount = 1              # (Discount factor)

        # Generate new batch of jobs
        self.dist = task_distribution.Dist(self.num_res, self.max_job_size, self.max_job_len)

        assert self.backlog_size % self.time_horizon == 0
        self.backlog_width = int(math.ceil(self.backlog_size / float(self.time_horizon)))
        self.network_input_height = self.time_horizon
        self.network_input_width = (self.res_slot + self.max_job_size * self.num_nw) * self.num_res + self.backlog_width + 1

        self.network_compact_dim = (self.num_res + 1) * (self.time_horizon + self.num_nw) + 1

        self.network_output_dim = self.num_nw + 1

        self.delay_penalty = -1       # (Delay penalty)
        self.hold_penalty = -1        # (Holding penalty)
        self.dismiss_penalty = -1     # (Dismiss penalty if queue is full)

        self.num_frames = 1           # (Number of frames to be combined and processed)
        self.lr_rate = 0.001          # (LEARNING RATE)
        self.rms_rho = 0.9            # (RMS PROP rho)
        self.rms_eps = 1e-9           # (RMS PROP epsilon)

        self.unseen = False  # Change seed in order to generate unseen data set

        # Supervised learning form policy
        self.batch_size = 10
        self.evaluate_policy_name = "SJF"

    def compute_dependent_parameters(self):
        assert self.backlog_size % self.time_horizon == 0

        self.backlog_width = int(self.backlog_size / self.time_horizon)

        self.network_input_height = self.time_horizon

        self.network_input_width = (self.res_slot + self.max_job_size * self.num_nw) * self.num_res + self.backlog_width + 1

        self.network_compact_dim = (self.num_res + 1) * (self.time_horizon + self.num_nw) + 1

        self.network_output_dim = self.num_nw + 1


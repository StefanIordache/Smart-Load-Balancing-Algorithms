
from Models.job import *
from Models.snapshot import *

from operator import attrgetter
import numpy as np
from collections import *


current_cluster_state = []
previous_cluster_state = []
jobs_waiting = deque()
jobs_running = deque()

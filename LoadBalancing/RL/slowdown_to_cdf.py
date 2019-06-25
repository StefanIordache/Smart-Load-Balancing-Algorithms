import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler

import environment
import parameters
import rl_network
import heuristic_agents


def discount(x, gamma):
    """
    Given vector x, computes a vector y such that
    y[i] = x[i] + gamma * x[i+1] + gamma^2 x[i+2] + ...
    """
    out = np.zeros(len(x))
    out[-1] = x[-1]
    for i in reversed(range(len(x)-1)):
        out[i] = x[i] + gamma*out[i+1]
    assert x.ndim >= 1

    return out


def categorical_sample(prob_n):
    """
    Sample from categorical distribution,
    specified by a vector of class probabilities
    """
    prob_n = np.asarray(prob_n)
    csprob_n = np.cumsum(prob_n)
    return (csprob_n > np.random.rand()).argmax()


def get_traj(test_type, pa, env, episode_max_length, rl_resume=None, render=False):
    """
    Run agent-environment loop for one whole episode (trajectory)
    Return dictionary of results
    """

    if test_type == 'RL':  # load trained parameters

        rl_learner = rl_network.RLLearner(pa)

        net_handle = open(rl_resume, 'rb')
        net_params = pickle.load(net_handle)
        rl_learner.set_net_params(net_params)

    env.reset()
    rews = []

    ob = env.observe()

    for _ in range(episode_max_length):

        if test_type == 'RL':
            a = rl_learner.choose_action(ob)

        elif test_type == 'Tetris':
            a = heuristic_agents.get_packer_action(env.machine, env.job_slot)

        elif test_type == 'SJF':
            a = heuristic_agents.get_sjf_action(env.machine, env.job_slot)

        elif test_type == 'Random':
            a = heuristic_agents.get_random_action(env.job_slot)

        ob, rew, done, info = env.step(a, repeat=True)

        rews.append(rew)

        if done:
            break
        if render:
            env.render()

    return np.array(rews), info


def launch(pa, rl_resume=None, render=False, plot=False, repre='image', end='no_new_job'):

    # ---- Parameters ----

    test_types = ['Tetris', 'SJF', 'Random']

    if rl_resume is not None:
        test_types = ['RL'] + test_types

    env = environment.Env(pa, render, repre=repre, end=end)

    all_discount_rews = {}
    jobs_slow_down = {}
    work_complete = {}
    work_remain = {}
    job_len_remain = {}
    num_job_remain = {}
    job_remain_delay = {}

    for test_type in test_types:
        all_discount_rews[test_type] = []
        jobs_slow_down[test_type] = []
        work_complete[test_type] = []
        work_remain[test_type] = []
        job_len_remain[test_type] = []
        num_job_remain[test_type] = []
        job_remain_delay[test_type] = []

    for seq_idx in range(pa.num_ex):
        print('\n\n')
        print("=============== " + str(seq_idx) + " ===============")

        for test_type in test_types:

            rews, info = get_traj(test_type, pa, env, pa.episode_max_length, rl_resume)

            print("---------- " + test_type + " -----------")

            print("total discount reward : \t %s" % (discount(rews, pa.discount)[0]))

            all_discount_rews[test_type].append(
                discount(rews, pa.discount)[0]
            )

            # ------------------------
            # ---- per job stat ----
            # ------------------------

            enter_time = np.array([info.record[i].enter_time for i in range(len(info.record))])
            finish_time = np.array([info.record[i].finish_time for i in range(len(info.record))])
            job_len = np.array([info.record[i].len for i in range(len(info.record))])
            job_total_size = np.array([np.sum(info.record[i].res_vec) for i in range(len(info.record))])

            finished_idx = (finish_time >= 0)
            unfinished_idx = (finish_time < 0)

            jobs_slow_down[test_type].append(
                (finish_time[finished_idx] - enter_time[finished_idx]) / job_len[finished_idx]
            )
            work_complete[test_type].append(
                np.sum(job_len[finished_idx] * job_total_size[finished_idx])
            )
            work_remain[test_type].append(
                np.sum(job_len[unfinished_idx] * job_total_size[unfinished_idx])
            )
            job_len_remain[test_type].append(
                np.sum(job_len[unfinished_idx])
            )
            num_job_remain[test_type].append(
                len(job_len[unfinished_idx])
            )
            job_remain_delay[test_type].append(
                np.sum(pa.episode_max_length - enter_time[unfinished_idx])
            )

        env.seq_no = (env.seq_no + 1) % env.pa.num_ex

    # -- matplotlib colormap no overlap --
    if plot:
        num_colors = len(test_types)
        cm = plt.get_cmap('gist_rainbow')
        fig = plt.figure()
        ax = fig.add_subplot(111)
        mpl.rcParams['axes.prop_cycle'] = cycler('color', [cm(1. * i / num_colors) for i in range(num_colors)])
        # ax.set_color_cycle([cm(1. * i / num_colors) for i in range(num_colors)])

        for test_type in test_types:
            slow_down_cdf = np.sort(np.concatenate(jobs_slow_down[test_type]))
            slow_down_yvals = np.arange(len(slow_down_cdf))/float(len(slow_down_cdf))
            ax.plot(slow_down_cdf, slow_down_yvals, linewidth=2, label=test_type)

        plt.legend(loc=4)
        plt.xlabel("job slowdown", fontsize=20)
        plt.ylabel("CDF", fontsize=20)
        # plt.show()
        print(rl_resume)
        plt.savefig(rl_resume + "_slowdown_fig" + ".pdf")

    return all_discount_rews, jobs_slow_down


def main():
    pa = parameters.Parameters()

    pa.simu_len = 200  # 5000  # 1000
    pa.num_ex = 10  # 100
    pa.num_nw = 10
    pa.num_seq_per_batch = 20
    # pa.max_nw_size = 5
    # pa.job_len = 5
    pa.new_job_rate = 0.3
    pa.discount = 1

    pa.episode_max_length = 20000  # 2000

    pa.compute_dependent_parameters()

    render = False

    plot = True  # plot slowdown cdf

    rl_resume = None
    rl_resume = 'data/rl_re_discount_1_rate_0.3_simu_len_200_num_seq_per_batch_20_ex_10_nw_10_1450.pkl'
    # rl_resume = 'data/rl_re_1000_discount_1_5990.pkl'

    pa.unseen = True

    launch(pa, rl_resume, render, plot, repre='image', end='all_done')


if __name__ == '__main__':
    main()
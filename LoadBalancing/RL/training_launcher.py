import os
import sys
import getopt
import matplotlib


import parameters
import policy_gradient_with_reinforcement_learning
import policy_gradient_with_supervised_learning
import slowdown_to_cdf


matplotlib.use('Agg')
os.environ["THEANO_FLAGS"] = "device=cuda,floatX=float32"

def script_usage():
    print('--training_type <type of training> \n'
          '--rl_file <parameter file for rl network> \n'
          '--v_file <parameter file for v network> \n'
          '--q_file <parameter file for q network> \n'
          '--out_freq <network output frequency> \n'
          '--out_file <output file name> \n'
          '--log <log file name> \n'
          '--render <plot dynamics> \n'
          '--new_example <generate unseen example> \n')


def main():

    pa = parameters.Parameters()

    type_exp = 'reinforce'  # 'supervised' 'test'

    rl_resume = None
    v_resume = None
    q_resume = None
    log = None

    render = False

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hi:o:", ["training_type=",
                      "rl_file=",
                      "v_file=",
                      "q_file=",
                      "out_freq=",
                      "out_file=",
                      "log=",
                      "render=",
                      "new_example="])

    except getopt.GetoptError:
        script_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            script_usage()
            sys.exit()
        elif opt in ("-e", "--training_type"):
            type_exp = arg
        elif opt in ("-p", "--rl_file"):
            rl_resume = arg
        elif opt in ("-v", "--v_file"):
            v_resume = arg
        elif opt in ("-q", "--q_file"):
            q_resume = arg
        elif opt in ("-f", "--out_freq"):
            pa.output_freq = int(arg)
        elif opt in ("-o", "--out_file"):
            pa.output_filename = arg
        elif opt in ("-lg", "--log"):
            log = arg
        elif opt in ("-r", "--render"):
            render = (arg == 'True')
        elif opt in ("-u", "--new_example"):
            pa.generate_unseen = (arg == 'True')
        else:
            script_usage()
            sys.exit()

    pa.compute_dependent_parameters()

    if type_exp == 'supervised':
        policy_gradient_with_supervised_learning.launch(pa, rl_resume, render, repre='image', end='all_done')
    elif type_exp == 'reinforce':
        policy_gradient_with_reinforcement_learning.launch(pa, rl_resume, render, repre='image', end='all_done')
    elif type_exp == 'test':
        slowdown_to_cdf.launch(pa, rl_resume, render, True)
    else:
        print("ERROR! Invalid training task: " + str(type_exp))
        exit(1)


if __name__ == '__main__':
    main()
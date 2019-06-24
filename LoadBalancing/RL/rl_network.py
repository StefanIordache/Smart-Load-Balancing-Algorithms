import numpy as np
import theano
import theano.tensor as T
import lasagne
from collections import OrderedDict


def rmsprop_updates(grads, params, step_size, rho=0.9, epsilon=0.9):

    updates = []

    for param, grad in zip(params, grads):
        accum = theano.shared(np.zeros(param.get_value(borrow=True).shape, dtype=param.dtype))
        accum_new = rho * accum + (1 - rho) * grad ** 2
        updates.append((accum, accum_new))
        updates.append((param, param + (step_size * grad / T.sqrt(accum_new + epsilon))))

    return updates


def utils_floatX(arr):
    return np.asarray(arr, dtype=theano.config.floatX)


def adam_update(grads, params, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):

    t_prev = theano.shared(utils_floatX(0.))
    updates = OrderedDict()

    # Using Theano constant to prevent up-casting of float32
    one = T.constant(1)

    t = t_prev + 1
    a_t = learning_rate*T.sqrt(one-beta2**t)/(one-beta1**t)

    for param, g_t in zip(params, grads):
        value = param.get_value(borrow=True)
        m_prev = theano.shared(np.zeros(value.shape, dtype=value.dtype),
                               broadcastable=param.broadcastable)
        v_prev = theano.shared(np.zeros(value.shape, dtype=value.dtype),
                               broadcastable=param.broadcastable)

        m_t = beta1*m_prev + (one-beta1)*g_t
        v_t = beta2*v_prev + (one-beta2)*g_t**2
        step = a_t*m_t/(T.sqrt(v_t) + epsilon)

        updates[m_prev] = m_t
        updates[v_prev] = v_t
        updates[param] = param + step

    updates[t_prev] = t

    return updates


class RLLearner:
    def __init__(self, pa):

        self.input_height = pa.network_input_height
        self.input_width = pa.network_input_width
        self.output_height = pa.network_output_dim

        self.num_frames = pa.num_frames

        self.update_counter = 0

        states = T.tensor4('states')
        actions = T.ivector('actions')
        values = T.vector('values')

        print('network_input_height=', pa.network_input_height)
        print('network_input_width=', pa.network_input_width)
        print('network_output_dim=', pa.network_output_dim)

        # image representation
        self.l_out = build_rl_network(pa.network_input_height, pa.network_input_width, pa.network_output_dim)

        self.lr_rate = pa.lr_rate
        self.rms_rho = pa.rms_rho
        self.rms_eps = pa.rms_eps

        params = lasagne.layers.helper.get_all_params(self.l_out)

        print(' params=', params, ' count=', lasagne.layers.count_params(self.l_out))

        self._get_param = theano.function([], params)

        # ===================================
        # TRAINING PART
        # ===================================

        prob_act = lasagne.layers.get_output(self.l_out, states)

        self._get_act_prob = theano.function([states], prob_act, allow_input_downcast=True)

        # --------  Policy Gradient  --------

        N = states.shape[0]

        loss = T.log(prob_act[T.arange(N), actions]).dot(values) / N

        grads = T.grad(loss, params)

        updates = rmsprop_updates(
            grads, params, self.lr_rate, self.rms_rho, self.rms_eps)

        self._train_fn = theano.function([states, actions, values], loss,
                                         updates=updates, allow_input_downcast=True)

        self._get_loss = theano.function([states, actions, values], loss, allow_input_downcast=True)

        self._get_grad = theano.function([states, actions, values], grads, allow_input_downcast=True)

        # --------  Supervised Learning  --------

        su_target = T.ivector('su_target')

        su_loss = lasagne.objectives.categorical_crossentropy(prob_act, su_target)
        su_loss = su_loss.mean()

        l2_penalty = lasagne.regularization.regularize_network_params(self.l_out, lasagne.regularization.l2)

        su_loss += 1e-3*l2_penalty
        print('learning_rate=', self.lr_rate)

        su_updates = lasagne.updates.rmsprop(su_loss, params,
                                             self.lr_rate, self.rms_rho, self.rms_eps)

        self._su_train_fn = theano.function([states, su_target], [su_loss, prob_act], updates=su_updates)

        self._su_loss = theano.function([states, su_target], [su_loss, prob_act])

        self._debug = theano.function([states], [states.flatten(2)])

    # Get action based on estimated probability
    def choose_action(self, state):

        act_prob = self.get_one_act_prob(state)

        csprob_n = np.cumsum(act_prob)
        act = (csprob_n > np.random.rand()).argmax()

        # print(act_prob, act)

        return act

    def train(self, states, actions, values):

        loss = self._train_fn(states, actions, values)
        return loss

    def get_params(self):

        return self._get_param()

    def get_grad(self, states, actions, values):

        return self._get_grad(states, actions, values)

    def get_one_act_prob(self, state):

        states = np.zeros((1, 1, self.input_height, self.input_width), dtype=theano.config.floatX)
        states[0, :, :] = state
        act_prob = self._get_act_prob(states)[0]

        return act_prob

    def get_act_probs(self, states):  # multiple states, assuming in floatX format
        act_probs = self._get_act_prob(states)
        return act_probs

    #  -------- Supervised Learning --------
    def su_train(self, states, target):
        loss, prob_act = self._su_train_fn(states, target)
        return np.sqrt(loss), prob_act

    def su_test(self, states, target):
        loss, prob_act = self._su_loss(states, target)
        return np.sqrt(loss), prob_act

    #  -------- Save/Load network parameters --------
    def return_net_params(self):
        return lasagne.layers.helper.get_all_param_values(self.l_out)

    def set_net_params(self, net_params):
        lasagne.layers.helper.set_all_param_values(self.l_out, net_params)


# ===================================
# build neural network
# ===================================


def build_rl_network(input_height, input_width, output_length):

    l_in = lasagne.layers.InputLayer(
        shape=(None, 1, input_height, input_width),
    )

    l_hid = lasagne.layers.DenseLayer(
        l_in,
        num_units=20,
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.Normal(.01),
        b=lasagne.init.Constant(0)
    )

    l_out = lasagne.layers.DenseLayer(
        l_hid,
        num_units=output_length,
        nonlinearity=lasagne.nonlinearities.softmax,
        W=lasagne.init.Normal(.01),
        b=lasagne.init.Constant(0)
    )

    return l_out


def build_compact_rl_network(input_height, input_width, output_length):
    l_in = lasagne.layers.InputLayer(
        shape=(None, 1, input_height, input_width),
        )

    l_hid1 = lasagne.layers.DenseLayer(
        l_in,
        num_units=520,
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.HeNormal('relu'),
        b=lasagne.init.Constant(0.05)
        )

    l_hid2 = lasagne.layers.DenseLayer(
        l_hid1,
        num_units=20,
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.HeNormal('relu'),
        b=lasagne.init.Constant(0.05)
        )

    l_hid3 = lasagne.layers.DenseLayer(
        l_hid2,
        num_units=20,
        nonlinearity=lasagne.nonlinearities.rectify,
        W=lasagne.init.HeNormal('relu'),
        b=lasagne.init.Constant(0.05)
        )

    l_out = lasagne.layers.DenseLayer(
        l_hid3,
        num_units=output_length,
        nonlinearity=lasagne.nonlinearities.softmax,
        W=lasagne.init.HeNormal('relu'),
        b=lasagne.init.Constant(0.05)
        )

    return l_out

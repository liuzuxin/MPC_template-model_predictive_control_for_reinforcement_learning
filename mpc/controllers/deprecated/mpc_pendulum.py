import numpy as np
from tqdm import trange, tqdm
from optimizers import RandomOptimizer, CEMOptimizer
import copy


class MPC(object):
    optimizers = {"CEM": CEMOptimizer, "Random": RandomOptimizer}

    def __init__(self, mpc_config):
        # mpc_config = config["mpc_config"]
        self.type = mpc_config["optimizer"]
        conf = mpc_config[self.type]
        self.horizon = conf["horizon"]
        self.gamma = conf["gamma"]
        self.action_low = np.array(conf["action_low"]) # array (dim,)
        self.action_high = np.array(conf["action_high"]) # array (dim,)
        self.action_dim = conf["action_dim"]
        self.popsize = conf["popsize"]
        self.env = conf["env"]
        self.action_cost = conf["action_cost"]
        self.x_dot_cost = conf["x_dot_cost"]
        self.particle = conf["particle"]

        self.init_mean = np.array([conf["init_mean"]] * self.horizon)
        self.init_var = np.array([conf["init_var"]] * self.horizon)

        if len(self.action_low) == 1: # auto fill in other dims
            self.action_low = np.tile(self.action_low, [self.action_dim])
            self.action_high = np.tile(self.action_high, [self.action_dim])
        
        self.optimizer = MPC.optimizers[self.type](sol_dim=self.horizon*self.action_dim,
                                                   popsize=self.popsize,
                                                   upper_bound=np.array(conf["action_high"]),
                                                   lower_bound=np.array(conf["action_low"]),
                                                   max_iters=conf["max_iters"],
                                                   num_elites=conf["num_elites"],
                                                   epsilon=conf["epsilon"],
                                                   alpha=conf["alpha"])

        # todo change the cost to the envirionment cost
        self.optimizer.setup(self.cost_function)
        self.reset()

    def reset(self):
        """Resets this controller (clears previous solution, calls all update functions).

        Returns: None
        """
        #print('set init mean to 0')
        self.prev_sol = np.tile((self.action_low + self.action_high) / 2, [self.horizon])
        self.init_var = np.tile(np.square(self.action_low - self.action_high) / 16, [self.horizon])

    def act(self, model, state):
        '''
        :param state: task, model, (numpy array) current state
        :return: (float) optimal action
        '''
        self.model = model
        self.state = state

        soln, var = self.optimizer.obtain_solution(self.prev_sol, self.init_var)
        if self.type == "CEM":
            self.prev_sol = np.concatenate([np.copy(soln)[self.action_dim:], np.zeros(self.action_dim)])
        else:
            pass
        action = soln[0]
        return action

    def preprocess(self, state):
        # given state return observation
        # state = (x, x_dot, theta, theta_dot)
        # obs = np.array([x, x_dot, np.cos(theta), np.sin(theta), theta_dot])
        obs = np.concatenate([state[:, 0:1], state[:, 1:2],
            np.cos(state[:, 2:3]), np.sin(state[:, 2:3]), state[:, 3:]], axis=1)
        # print('obs shape ', obs.shape)
        return obs

    def cost_function(self, actions):
        """
        Calculate the cost given a sequence of actions

        Parameters:
        ----------
            @param numpy array - actions : size should be (batch_size x horizon number)

        Return:
        ----------
            @param numpy array - cost : length should be of batch_size
        """
        def angle_normalize(x):
            return (((x+np.pi) % (2*np.pi)) - np.pi)

        batch_size = actions.shape[0]
        costs = np.zeros(batch_size)
        state = np.repeat(self.state.reshape(1,-1), batch_size, axis=0)
        for t in range(self.horizon):
            action = actions[:,t].reshape(-1,1) # numpy array (batch_size x action dim)
            state_next = self.model.predict(state, action)+state  # numpy array (batch_size x state dim)
            state_next[:,0] = angle_normalize(state_next[:,0])
            cost = self.pendulum_cost(state_next, action) # compute cost
            costs = costs + cost*self.gamma
            state = state_next
        return costs

    def pendulum_cost(self, state, action):
        """
        Calculate the pendulum env cost given the state

        Parameters:
        ----------
            @param numpy array - state : size should be (batch_size x state dim)
            @param numpy array - action : size should be (batch_size x action dim)

        Return:
        ----------
            @param numpy array - cost : length should be of batch_size
        """
        
        th = state[:,0]
        thdot = state[:,1]
        u = action[:,0]
        cost = th**2 + .1*thdot**2 + .001*(u**2)
        #reward = -np.sqrt(2*(1.0 - cos_theta))
        #cost = - reward
        return cost

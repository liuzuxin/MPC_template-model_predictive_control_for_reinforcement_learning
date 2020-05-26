'''
@Author: Zuxin Liu
@Email: zuxinl@andrew.cmu.edu
@Date:   2020-03-24 10:49:12
@LastEditTime: 2020-05-08 14:37:14
@Description:
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np
import torch
import time

from .optimizer import Optimizer


class RandomOptimizer(Optimizer):
    def __init__(self, sol_dim, popsize, upper_bound=None, lower_bound=None, max_iters=10, num_elites=100, epsilon=0.001, alpha=0.25):
        """Creates an instance of this class.

        Arguments:
            sol_dim (int): The dimensionality of the problem space
            popsize (int): The number of candidate solutions to be sampled at every iteration
            upper_bound (np.array): An array of upper bounds
            lower_bound (np.array): An array of lower bounds
            other parameters are not used in this optimizer
        """
        super().__init__()
        self.sol_dim = sol_dim
        self.popsize = popsize
        self.ub, self.lb = torch.FloatTensor(upper_bound), torch.FloatTensor(lower_bound)
        self.solution = None
        self.cost_function = None

    def setup(self, cost_function):
        """Sets up this optimizer using a given cost function.

        Arguments:
            cost_function (func): A function for computing costs over a batch of candidate solutions.

        Returns: None
        """
        #print("lb, ub", self.lb, self.ub)
        self.cost_function = cost_function
        self.sampler = torch.distributions.uniform.Uniform(self.lb, self.ub)
        self.size = [self.popsize, self.sol_dim]

    def reset(self):
        pass

    def obtain_solution(self, *args, **kwargs):
        """Optimizes the cost function provided in setup().

        Arguments:
            init_mean (np.ndarray): The mean of the initial candidate distribution.
            init_var (np.ndarray): The variance of the initial candidate distribution.
        """
   
        solutions = self.sampler.sample(self.size).cpu().numpy()[:,:,0]
        #solutions = np.random.uniform(self.lb, self.ub, [self.popsize, self.sol_dim])
        costs = self.cost_function(solutions)
        return solutions[np.argmin(costs)], None

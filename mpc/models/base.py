'''
@Author: Zuxin Liu
@Email: zuxinl@andrew.cmu.edu
@Date:   2020-03-24 01:02:16
@LastEditTime: 2020-03-24 10:50:21
@Description:
'''

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import torch
import torch.nn as nn

def mlp(sizes, activation, output_activation=nn.Identity):
    layers = []
    for j in range(len(sizes)-1):
        act = activation if j < len(sizes)-2 else output_activation
        layers += [nn.Linear(sizes[j], sizes[j+1]), act()]
    return nn.Sequential(*layers)

class MLPRegression(nn.Module):

    def __init__(self, input_dim, output_dim, hidden_sizes=(64,64), activation=nn.Tanh):
        """
            @param int - input_dim
            @param int - output_dim 
            @param list - hidden_sizes : such as [32,32,32]
        """ 
        super().__init__()
        self.net = mlp([input_dim] + list(hidden_sizes) + [output_dim], activation)

    def forward(self, x):
        """
            @param tensor - x: shape [batch, input dim]

            @return tensor - out : shape [batch, output dim]
        """ 
        out = self.net(x)
        return out

class MLPCategorical(nn.Module):

    def __init__(self, input_dim, output_dim, hidden_sizes=(64,64), activation=nn.Tanh):
        """
            @param int - input_dim
            @param int - output_dim 
            @param list - hidden_sizes : such as [32,32,32]
        """ 
        super().__init__()
        self.logits_net = mlp([input_dim] + list(hidden_sizes) + [output_dim], activation)

    def forward(self, x):
        """
            @param tensor - x: shape [batch, input dim]

            @return tensor - out : shape [batch, 1]
        """ 
        logits = self.logits_net(x)
        out = Categorical(logits=logits)
        return torch.squeeze(out, -1)

class Model:
    
    def __init__(self, *args, **kwargs):
        pass

    def predict(self, state, action):
        """
        Predict a batch of state and action pairs and return numpy array

        Parameters:
        ----------
            @param tensor or numpy - state : size should be (batch_size x state dim)
            @param tensor or numpy - action : size should be (batch_size x action dim)

        Return:
        ----------
            @param numpy array - state_next - size should be (batch_size x state dim)
        """
        raise NotImplementedError("Must be implemented in subclass.")

    def fit(self, data, label):
        """
        Fit the model given data and label

        Parameters:
        ----------
            @param list of numpy array - data : each array size should be of (state dim + action dim)
            @param list of numpy array - label : each array size should be of (state dim)

        Return:
        ----------
            @param (int, int) - (training loss, test loss)
        """
        raise NotImplementedError("Must be implemented in subclass.")

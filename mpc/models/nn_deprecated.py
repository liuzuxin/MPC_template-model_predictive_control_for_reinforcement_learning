'''
@Author: Zuxin Liu
@Email: zuxinl@andrew.cmu.edu
@Date:   2020-03-24 01:01:42
@LastEditTime: 2020-04-01 16:49:41
@Description:
'''

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import numpy as np

import torch
import torch.nn as nn
import torch.autograd as autograd

from .model import Model
from tqdm import tqdm
from tqdm import trange
from utils import *


class MLP(nn.Module):
    '''A simple implementation of the multi-layer neural network'''
    def __init__(self, n_input=7, n_output=6, n_h=2, size_h=128):
        '''
        Specify the neural network architecture

        :param n_input: The dimension of the input
        :param n_output: The dimension of the output
        :param n_h: The number of the hidden layer
        :param size_h: The dimension of the hidden layer
        '''
        super(MLP, self).__init__()
        self.n_input = n_input
        self.fc_in = nn.Linear(n_input, size_h)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()
        assert n_h >= 1, "h must be integer and >= 1"
        self.fc_list = nn.ModuleList()
        for i in range(n_h - 1):
            self.fc_list.append(nn.Linear(size_h, size_h))
        self.fc_out = nn.Linear(size_h, n_output)
        # Initialize weight
        nn.init.uniform_(self.fc_in.weight, -0.1, 0.1)
        nn.init.uniform_(self.fc_out.weight, -0.1, 0.1)
        self.fc_list.apply(self.init_normal)

    def forward(self, x):
        out = x.view(-1, self.n_input)
        out = self.fc_in(out)
        out = self.tanh(out)
        for _, layer in enumerate(self.fc_list, start=0):
            out = layer(out)
            out = self.tanh(out)
        out = self.fc_out(out)
        return out

    def init_normal(self, m):
        if type(m) == nn.Linear:
            nn.init.uniform_(m.weight, -0.1, 0.1)


class DynamicModel(Model):
    def __init__(self, config):
        super().__init__()
        model_config = config["model_config"]
        self.n_states = model_config["n_states"]
        self.n_actions = model_config["n_actions"]
        self.use_cuda = model_config["use_cuda"]

        if model_config["load_model"]:
            self.model = torch.load(model_config["model_path"])
        else:
            self.model = MLP(self.n_states + self.n_actions, self.n_states, model_config["n_hidden"], model_config["size_hidden"])
        if self.use_cuda:
            self.model = self.model.cuda()
            self.Variable = lambda *args, **kwargs: autograd.Variable(*args, **kwargs).cuda()
        else:
            self.model = self.model.cpu()
            self.Variable = lambda *args, **kwargs: autograd.Variable(*args, **kwargs)
        training_config = config["training_config"]
        self.n_epochs = training_config["n_epochs"]
        self.lr = training_config["learning_rate"]
        self.batch_size = training_config["batch_size"]
        self.save_model_flag = training_config["save_model_flag"]
        self.save_model_path = training_config["save_model_path"]
        self.exp_number = training_config["exp_number"]
        self.save_loss_fig = training_config["save_loss_fig"]
        self.save_loss_fig_frequency = training_config["save_loss_fig_frequency"]
        self.criterion = nn.MSELoss(reduction='mean')
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.lr)
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


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
        result_tensor = self.predict_batch(state, action)
        result = result_tensor.cpu().detach().numpy()
        return result

    def predict_batch(self, state, action):
        """
        Predict a batch of state and action pairs and return tensor

        Parameters:
        ----------
            @param tensor or numpy array - state : size should be (batch_size x state dim)
            @param tensor or numpy array - action : size should be (batch_size x action dim)

        Return:
        ----------
            @param tensor - state_next - size should be (batch_size x state dim)
        """
        action = action.reshape(-1,1) # batch_size x action space dim
        assert (state.shape[0] == action.shape[0]), "The batch size shape should be the same"
        if not torch.is_tensor(state):
            state = torch.tensor(state).float().to(self.device)
        if not torch.is_tensor(action):
            action = torch.tensor(action).float().to(self.device)
        inputs = torch.cat( (state,action),axis=1 )
        state_next = self.model(inputs)
        return state_next

    def reset_model(self):
        def weight_reset(m):
            if type(m) == nn.Linear:
                nn.init.uniform_(m.weight, -1, 1)
        self.model.apply(weight_reset)

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
        #self.reset_model()
        num_data = len(data)
        data_tensor = torch.tensor(data).float().to(self.device)
        label_tensor = torch.tensor(label).float().to(self.device)
        indices = list(range(num_data))
        valid_size = 0.2
        split = int(np.floor(valid_size * num_data))
        np.random.shuffle(indices)
        train_idx, test_idx = indices[split:], indices[:split]

        train_set = []
        test_set = []

        for idx in train_idx:
            train_set.append([data_tensor[idx], label_tensor[idx]])
            
        for idx in test_idx:
            test_set.append([data_tensor[idx], label_tensor[idx]])
        
        train_loader = torch.utils.data.DataLoader(train_set, shuffle=True, batch_size=self.batch_size)
        test_loader = torch.utils.data.DataLoader(test_set, shuffle=True, batch_size=self.batch_size)

        total_step = len(train_loader)
        
        loss_epochs = []

        #t = trange(self.n_epochs)
        
        t = tqdm(range(self.n_epochs), position=1)

        #t.write("Fitting the model... Total training step per epoch [%i] with batch size [%i]"%(total_step, self.batch_size))
        #t.write("****************************************")

        for epoch in t:
            loss_this_epoch = []
            for i, (datas, labels) in enumerate(train_loader):
                #datas = self.Variable(torch.FloatTensor(np.float32(datas)))
                #labels = self.Variable(torch.FloatTensor(np.float32(labels)))
                self.optimizer.zero_grad()
                outputs = self.model(datas)
                loss = self.criterion(outputs, labels)
                loss.backward()
                self.optimizer.step()
                loss_this_epoch.append(loss.item())
            loss_epochs.append(np.mean(loss_this_epoch))
            if self.save_model_flag:
                torch.save(self.model, self.save_model_path)
            if self.save_loss_fig and epoch % self.save_loss_fig_frequency == 0:
                self.save_figure(epoch, loss_epochs, loss_this_epoch)

                loss_test = self.validate_model(test_loader)
                
            t.set_description(f"training epoch [{epoch}/{self.n_epochs}], loss train: {np.mean(loss_this_epoch):.4f}, loss test  {loss_test:.4f}")
            #t.update(1)

        return np.mean(loss_this_epoch), loss_test

    def validate_model(self, testloader):
        '''
        Validate the trained model

        :param datasets: (numpy array) input data
        :param labels: (numpy array) corresponding label
        :return: average loss
        '''
        loss_list = []
        for sample in testloader:
            inputs, labels = sample
            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)
            loss_list.append(loss.item())
        return np.mean(loss_list)
        
    def save_figure(self, epoch, loss_epochs,loss_this_epoch):
        '''
        Save the loss figures
        '''
        plt.clf()
        plt.close("all")
        plt.figure(figsize=(12, 5))
        plt.subplot(121)
        plt.title('Loss Trend with %s Epochs' % (epoch))
        plt.plot(loss_epochs)
        plt.subplot(122)
        plt.title('Loss Trend in the latest Epoch')
        plt.plot(loss_this_epoch)
        plt.savefig("storage/loss-" + str(self.exp_number) + ".png")
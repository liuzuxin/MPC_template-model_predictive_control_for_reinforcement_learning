# MPC
This repo contains the implementation of Pytorch version of the MPC algorithm and the evaluation on the CartPole Swingup environment.

The MPC implementation is partly followed in this paper [here](https://arxiv.org/abs/1805.12114) and its [repo](https://github.com/kchua/handful-of-trials)

All the hyper-parameters and experiment setting are stored in the ```./config``` folder.

All the results (figure and model) will be stored in the ```./storage``` folder by default.

The training and testing scripts are stored in the ```./scripts ``` folder.

### Requirements

* pytorch
* OpenAI gym

### How to run

For the Cartpole swingup environment, simply go to the script folder and run

```angularjs
cd script && python train.py
```
The script will load the configurations in the ```./config/config.yml``` file and begin to train.

By default, I only implemented the reward function for CartPole Swingup. Alternatively, you can train a NN-based reward model according to the needs of your environment. To do so, first run:
```angularjs
python train.py --train_reward_model 1
```
Then the reward model will be saved in the ```./storage``` folder by default. Then you can run:
```angularjs
python train.py --use_reward_model 1
```
The MPC controller will use the learned reward function to perform optimizations.

### Configuration explanation

In the ```config.yml``` file, there are 4 sets of configuration.

The `model_config`  part is the configuration of the parameters which determines the neural network architecture and the environment basis.

The `training_config` part is the configuration of the training process parameters.

The `mpc_config` part is the configuration of the MPC algorithm parameters, where you can choose to use the CEM optimizer or the Random optimizer.

If you want to train your model from scratch, then set the `load_model` parameter to `False`. If set to `True`, the trainer will load the model from `model_path`.

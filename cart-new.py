import gym
import time
from perceptrons import *
from datetime import datetime

def runTrial(env, tron):
    obs = env.reset()
    totalRewards = 0
    while True:
        env.render()
        act = tron(obs)
        obs, reward, done, info = env.step(act)
        totalRewards += reward
        if done or totalRewards >= 1000:
            return totalRewards

    # obs = observation of the state of the world
    # reward = a number indicating how well we're doing
    # done = boolean, true = game over
    # info = some debugging information

random.seed(datetime.now())
env = gym.make('CartPole-v0')
tron = Perceptron(numInputs=4, learningRate=1.0,
                  transfer=TwoStepFun(0))

trialNum = 0
bestReward = 0
bestWeights = tron.weights[:] # copy list of weights
while True:
    reward = runTrial(env, tron)
    print("Trial %d: reward=%d  ..... BEST=%d" %
          (trialNum, reward, bestReward))
    if reward > bestReward:     # remember best
        print(" ++ %s" % tron.weights)
        bestReward = reward
        bestWeights = tron.weights[:]
    else:                       # revert to best
        print(" -- %s" % bestWeights)
        tron.weights = bestWeights[:]
    tron.fuzzAll()
    trialNum += 1

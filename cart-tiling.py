# cart-tiling
import gym
import time
import random
import numpy as np
from perceptrons import *

NUM_TILES = 10
LEARNING_RATE = 0.5
RENDER = False

np.set_printoptions(threshold=np.nan)

def tile_observations(obs):
    o0 = int((obs[0] + 2.4)*NUM_TILES/4.8) # -2.4 .. +2.4
    o1 = int((obs[1] + 3.2)*NUM_TILES/6.4) # -3.2 .. +3.2
    o2 = int((obs[2] + 0.25)*NUM_TILES*2)  # -.25 .. +.25
    o3 = int((obs[3] + 3.7)*NUM_TILES/7.4) # -3.7 .. +3.7
    st = (o0 * NUM_TILES ** 0 +
          o1 * NUM_TILES ** 1 +
          o2 * NUM_TILES ** 2 +
          o3 * NUM_TILES ** 3)
    # Debug out of range
    if st >= NUM_TILES ** 4:
        print "YIKES! Out of range:", obs
    return st

def episode_expected_table(env, est, policy):
    # est is estimated values of each state
    obs = env.reset()
    data = []
    while True:
        if RENDER:
            env.render()
        st = tile_observations(obs)
        # What does policy say to do in this state?
        p = policy[st]  # This is a probability of going LEFT.
        r = random.random()  # Random between 0..1
        act = 0 if r < p else 1
        obs, reward, done, info = env.step(act)
        data.append((st,act,reward)) # 0:state, 1:action, 2:reward
        if done:
            break
    # Episode is over, now work backwards
    accum = 0
    for i in range(len(data)-1, -1, -1):
        accum += data[i][2]
        data[i] = (data[i][0], data[i][1], data[i][2], accum)
        # Update the estimate for this state-action pair
        # TODO (maybe): we're not using a future discount
        est[data[i][0]][data[i][1]] += LEARNING_RATE * accum
    return accum

random.seed(time.time())
env = gym.make('CartPole-v0')
# Because we don't know the exact state transitions,
# we'll estimate values of state-action pairs.
NUM_STATES = NUM_TILES ** 4
NUM_ACTIONS = 2
est = np.zeros([NUM_STATES, NUM_ACTIONS])
policy = np.full([NUM_STATES], 0.5) # Equi-probable between L/R
while True:
  # Value estimation
  total = 0
  for _ in range(250):
      total += episode_expected_table(env, est, policy)
  total /= 250
  print "Estimating: average reward is", total
  #if total > 250:
  #    RENDER = True
  # Policy improvement -- for each state, see if one action
  # is better than the other.
  print "Improve"
  for s in range(NUM_STATES):
      # Make policy probability proportional to the reward
      if est[s].sum() != 0:     # TODO (maybe): within some margin
          policy[s] = est[s][0] / est[s].sum()
      #if est[s][0] > est[s][1]:   # LEFT is better
      #    policy[s] += 0.1
      #else:                       # RIGHT is better
      #    policy[s] -= 0.1
  #print policy

print(est)
print(len(est))

#for _ in range(100):
#    obs = env.reset()
#    while True:
#        env.render()
#        act = env.action_space.sample() # random move
#        obs, reward, done, info = env.step(act)
#        st = tile_observations(obs)
#        print st, obs, act, reward
#        if done:
#            break
#

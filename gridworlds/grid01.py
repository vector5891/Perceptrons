# grid01.py -- figure 3.5 from RL book.

NUM_STATES = 25
ACTIONS = ['N', 'S', 'E', 'W']
GAMMA = 0.9                     # future discount rate

def step(state, action):  # returns (newState, reward)
    if state == 1:        # teleport "A"
        return (21, 10)
    if state == 3:              # teleport "B"
        return (13, 5)
    if action == 'W' and state%5 == 0: # left column
        return (state, -1)
    if action == 'N' and state < 5: # top row
        return (state, -1)
    if action == 'E' and state%5 == 4: # right column
        return (state, -1)
    if action == 'S' and state >= 20: # bottom row
        return (state, -1)
    # The rest are legit actions with zero reward/penalty.
    if action == 'S':
        return (state+5, 0)
    if action == 'N':
        return (state-5, 0)
    if action == 'E':
        return (state+1, 0)
    if action == 'W':
        return (state-1, 0)
    assert False #impossible?

def value_function_equiprobable_one_pass(estimates):
    for st in range(NUM_STATES):
        stateN, rewardN = step(st, 'N')
        stateS, rewardS = step(st, 'S')
        stateE, rewardE = step(st, 'E')
        stateW, rewardW = step(st, 'W')
        avg = (rewardN + GAMMA * estimates[stateN] +
               rewardS + GAMMA * estimates[stateS] +
               rewardE + GAMMA * estimates[stateE] +
               rewardW + GAMMA * estimates[stateW]) / 4
        #print(avg)
        estimates[st] = avg

if __name__ == "__main__":
    import numpy as np
    est = np.zeros([NUM_STATES])
    for _ in range(100):        # number of iterations
        value_function_equiprobable_one_pass(est)
    print(est)

# grid-m4.py

NUM_STATES = 50
# It's actually still a 5x5 grid, but we use the first half
# to number states before the treasure is taken, and the
# second half (25..49) to number states after treasure is taken.

# To be specific, if the treasure is in position 11, when you enter
# that position (for example going east from 10) you actually
# transition to state 36 (11+25) because now the treasure is consumed.
# There's no way to get back to states < 25.

# Also the goal state gets duplicated. It's at position 12, but that
# state# represents not having the treasure. So if you go to 12 you'd
# end the game with no reward. What we really want is to get to state
# 37 (12+25), that's where we get the reward for ending the game.

ACTIONS = ['N', 'S', 'E', 'W']
GAMMA = 0.9                     # future discount rate

def step(state, action):        # returns (newState, reward)
    if state%25 == 12:          # Game over, man. GAME OVER!
        return (state, 0)
    if (state == 32 and action == 'S' or
        state == 38 and action == 'W'): # Final move, have treasure
        return (37, 20)
    if (state == 6 and action == 'S' or
        state == 10 and action == 'E' or
        state == 16 and action == 'N'): # Pick up treasure
        return (36, 5)
    # Now we do penalties for the interior walls
    if (action == 'E' and state%25 in [6,11] or
        action == 'W' and state%25 in [7,12] or
        action == 'N' and state%25 in [17,18] or
        action == 'S' and state%25 in [12,13]):
        return (state, -1)
    # Now penalties for going off-grid
    if (action == 'W' and state%5 == 0 or # left column
        action == 'N' and state%25 < 5 or # top row
        action == 'E' and state%5 == 4 or # right column
        action == 'S' and state%25 >= 20): # bottom row
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

def value_function_one_pass(estimates, policies):
    for st in range(NUM_STATES):
        stateN, rewardN = step(st, 'N')
        stateS, rewardS = step(st, 'S')
        stateE, rewardE = step(st, 'E')
        stateW, rewardW = step(st, 'W')
        avg = (policies[st][0] * (rewardN + GAMMA * estimates[stateN]) +
               policies[st][1] * (rewardS + GAMMA * estimates[stateS]) +
               policies[st][2] * (rewardE + GAMMA * estimates[stateE]) +
               policies[st][3] * (rewardW + GAMMA * estimates[stateW]))
        #print(avg)
        estimates[st] = avg

def best_action(state, estimates):
    bestAct = None
    bestScore = float('-inf')
    for act in ACTIONS:
        newState, reward = step(state, act)
        score = estimates[newState] + reward
        if score > bestScore:
            bestAct = act
            bestScore = score
    return bestAct

def arrows(act):
    if act == 'N': return '↑'
    elif act == 'S': return '↓'
    elif act == 'E': return '→'
    elif act == 'W': return '←'
    else: assert False

def action_index(act):
    if act == 'N': return 0
    elif act == 'S': return 1
    elif act == 'E': return 2
    elif act == 'W': return 3
    else: assert False

def evaluate_policy(est, policies):
    for _ in range(100):        # number of iterations
        value_function_one_pass(est, policies)

def improve_policy(est, policies):
    for st in range(NUM_STATES):
        act = action_index(best_action(st, est))
        # Increment the probability of that action
        policies[st][act] += 0.1
        # Renormalize so they add to 1.
        policies[st] = policies[st] / policies[st].sum()

def show_estimates(est):
    for row in range(5):
        for col in range(5):
            s = row*5 + col
            a = arrows(best_action(s, est))
            sys.stdout.write('%5.1f%c ' % (est[s], a))
        sys.stdout.write('    ')
        for col in range(5):
            s = row*5 + col + 25
            a = arrows(best_action(s, est))
            sys.stdout.write('%5.1f%c ' % (est[s], a))
        sys.stdout.write('\n')


if __name__ == "__main__":
    import numpy as np
    import sys
    est = np.zeros([NUM_STATES])
    policies = np.full([NUM_STATES, len(ACTIONS)], 1.0 / len(ACTIONS))
    for _ in range(20):
        show_estimates(est)
        print("Evaluating...")
        evaluate_policy(est, policies)
        print("Improving...")
        improve_policy(est, policies)
    #print(est)

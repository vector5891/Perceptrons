import random

NUM_PULLS = 60000
NUM_GAMES = 7

def evaluate(agent, bandit):
    print("Evaluation =======> %s" % agent.__name__)
    avg = 0.0
    for game in range(NUM_GAMES):
        # We'll shuffle the positions of its layers, so you can't rely on the
        # optimal one being at a particular index.
        random.shuffle(bandit.levers)
        a = agent(len(bandit.levers))
        rewards = [0.0]
        for _ in range(NUM_PULLS):
            used = [False]
            def pull(lever):
                assert not used[0] # Don't pull more than once per play!
                payout = bandit.pull(lever)
                used[0] = True
                rewards[0] += payout
                return payout
            a.play(pull)
        rewards[0] /= NUM_PULLS
        print(" Game %d: %f %s" % (game, rewards[0], a.report()))
        avg += rewards[0]
    avg /= NUM_GAMES
    print("Average: %f" % avg)
    return avg

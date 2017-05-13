# Initial framework for minesweeper
from gym.spaces import Discrete
from gym.spaces.tuple_space import Tuple
from gym.spaces import seed
import numpy as np
import random

class Minefield(object):
    UNKNOWN = -1
    MINE = -99

    def __init__(self, rows=8, cols=8, mines=10):
        seed()                  # Initialize RNG
        self.action_space = Tuple((Discrete(rows),Discrete(cols)))
        self.rows = rows
        self.cols = cols
        self.mines = mines

    def reset(self):
        # Internal state: where are all the mines?
        self.mine_coords = set()
        mines_to_place = self.mines
        while mines_to_place > 0:
            r = random.randrange(self.rows)
            c = random.randrange(self.cols)
            if (r,c) not in self.mine_coords: # new coord
                self.mine_coords.add((r,c))
                mines_to_place -= 1
        # DONE: don't duplicate mine coordinates. If a mine
        # is already in a given (r,c), choose a different coord.
        print("SECRET locations:", self.mine_coords)
        # External state: where has user clicked? What did they see
        # there? We use -1 to indicate UNKNOWN (before clicking),
        # -99 to indicate a MINE, or 0..8 to represent #neighbors
        # that have mines.
        self.state = np.full([self.rows, self.cols], Minefield.UNKNOWN)
        self.coords_to_clear = self.rows * self.cols - self.mines
        return self.state

    def step(self, coord):        # returns obs, reward, done, info
        # DONE: modify self.state, calculate reward, determine if game
        # over. Rewards are: -99 if click a mine (and game over), +50
        # if all spaces are cleared except for mines (and game over),
        # +1 if space is cleared successfully, -2 for clicking on a
        # coord that is already cleared.
        reward = 0
        done = False
        if self.state[coord] != Minefield.UNKNOWN:
            reward = -2
        elif coord in self.mine_coords:
            # Clicked on a mine!
            self.state[coord] = Minefield.MINE
            reward = Minefield.MINE # -99
            done = True
        else:
            neighboring_mines = 0
            for r in range(coord[0]-1, coord[0]+2):
                for c in range(coord[1]-1, coord[1]+2):
                    if (r,c) in self.mine_coords:
                        neighboring_mines += 1
            self.state[coord] = neighboring_mines
            self.coords_to_clear -= 1
            if self.coords_to_clear == 0:
                reward = 50     # Yay you won.
                done = True
            else:
                reward = 1
        return (self.state, reward, done, None)

    def render(self):
        print(self.state)       # TODO: make it prettier
        # Here's an example of what I mean by 'prettier'...
        # with this we could define a human interface to game also.
        # a........
        # b........
        # c...X....
        # d........
        # e.2..._..
        # f........
        # g........
        # h........
        #  01234567

if __name__ == "__main__":
    from constraints import Constraints
    constraints = Constraints()
    env = Minefield()
    obs = env.reset()
    env.render()
    done = False
    total = 0
    while not done:
        # Choose random action
        act = env.action_space.sample()
        obs, reward, done, info = env.step(act)
        total += reward
        if not done:
            # Add the fact to the constraint DB.
            neighbors = []
            for r in range(act[0]-1, act[0]+2):
                for c in range(act[1]-1, act[1]+2):
                    if (r,c) != act:
                        neighbors.append((r,c))
            constraints.add(obs[act], neighbors)
        print(act, reward, done)
        constraints.show()
        env.render()
    print("Game over, total is", total)

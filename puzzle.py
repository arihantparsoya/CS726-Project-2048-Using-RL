import random

import logic
import constants as c

class GameGrid():
    def __init__(self):
        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down,
                         c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right,
                         c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down,
                         c.KEY_LEFT_ALT: logic.left,
                         c.KEY_RIGHT_ALT: logic.right}

        self.actions = [c.KEY_UP, c.KEY_DOWN, c.KEY_RIGHT, c.KEY_LEFT]
        self.grid_cells = []
        self.init_matrix()

    def gen(self):
        return random.randint(0, c.GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = logic.new_game(4)
        self.matrix = logic.add_two(self.matrix)
        self.matrix = logic.add_two(self.matrix)

    def step(self, key):
        if isinstance(key, int):
            key = self.actions[key]

        if key in self.commands:
            self.matrix, done = self.commands[key](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
                done = False

                # Check if game is completed
                if logic.game_state(self.matrix) == 'win':
                    done = True
                if logic.game_state(self.matrix) == 'lose':
                    done = True

            return self.matrix, logic.reward(self.matrix), done, ""

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

    def get_state(self):
        return self.matrix

    def key_down(self, event):
        key = repr(event.char)
        if event.keycode == 114:
            self.reset()
            return
        self.step(key)
        self.display_state()

    def action_space(self):
        # return possible action
        return self.actions[random.randint(0, 3)]

    def reset(self):
        # resets the game to initial state
        self.init_matrix()
        return self.matrix

    def display_state(self):
        print()
        for i in self.matrix:
            print(i)

    def reward(self):
        return logic.reward(self.matrix)

    def highest_score(self):
        return logic.highest_score(self.matrix)

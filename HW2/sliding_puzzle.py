import random
import logging
import sys
import os
import math
from collections import deque
import argparse
import pickle


class QLearning:
    def __init__(self, num_actions=4, learning_rate=0.1, discount_factor=0.9):
        self.matrix = {}
        self.num_actions = num_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def update(self, state, action, reward, next_state):
        if state not in self.matrix:
            self.matrix[state] = [0] * self.num_actions
        if next_state not in self.matrix:
            self.matrix[next_state] = [0] * self.num_actions

        q_s_a = self.matrix[state][action]
        max_q_next = max(self.matrix[next_state])
        alpha = self.learning_rate
        r = reward
        gamma = self.discount_factor
        self.matrix[state][action] = (1 - alpha)*q_s_a + alpha*(r + gamma*max_q_next)


class Puzzle:
    def __init__(self, init_state=(7, 2, 4, 5, 0, 6, 8, 3, 1), size=3, blank_pos=None):

        # State Definition
        # A puzzle state like this
        # a b c
        # d e f
        # g h i
        # will be flattend to 'abcdefghi' to represent the state.

        # Assume init_state and size make sense
        self.state = init_state
        self.size = size
        self.blank_pos = self.idx_to_pos(self.state.index(0)) if blank_pos is None else blank_pos

    @property
    def goal_state(self):
        return (0, 1, 2, 3, 4, 5, 6, 7, 8)

    def idx_to_pos(self, idx):
        return idx // self.size, idx % self.size

    def pos_to_idx(self, row, col):
        return row * self.size + col

    def next_states_actions(self):
        r, c = self.blank_pos
        ret = []
        # Up
        if r > 0:
            # swap the blank with the piece on top
            state = list(self.state)
            state[self.pos_to_idx(r, c)] = self.state[self.pos_to_idx(r - 1, c)]
            state[self.pos_to_idx(r - 1, c)] = 0
            p = Puzzle(tuple(state), self.size, (r - 1, c))
            ret.append((p, 0))
        # Right
        if c < self.size - 1:
            # swap the blank with the piece on the right
            state = list(self.state)
            state[self.pos_to_idx(r, c)] = self.state[self.pos_to_idx(r, c + 1)]
            state[self.pos_to_idx(r, c + 1)] = 0
            p = Puzzle(tuple(state), self.size, (r, c + 1))
            ret.append((p, 1))
        # Down
        if r < self.size - 1:
            # swap the blank with the piece below
            state = list(self.state)
            state[self.pos_to_idx(r, c)] = self.state[self.pos_to_idx(r + 1, c)]
            state[self.pos_to_idx(r + 1, c)] = 0
            p = Puzzle(tuple(state), self.size, (r + 1, c))
            ret.append((p, 2))
        # Left
        if c > 0:
            # swap the blank with the piece on the left
            state = list(self.state)
            state[self.pos_to_idx(r, c)] = self.state[self.pos_to_idx(r, c - 1)]
            state[self.pos_to_idx(r, c - 1)] = 0
            p = Puzzle(tuple(state), self.size, (r, c - 1))
            ret.append((p, 3))
        return ret

    def move(self, action):
        # assume action is legal
        r, c = self.blank_pos
        if action == 0:
            state = list(self.state)
            state[self.pos_to_idx(r, c)] = self.state[self.pos_to_idx(r - 1, c)]
            state[self.pos_to_idx(r - 1, c)] = 0
            self.blank_pos = r - 1, c
            self.state = tuple(state)
        elif action == 1:
            state = list(self.state)
            state[self.pos_to_idx(r, c)] = self.state[self.pos_to_idx(r, c + 1)]
            state[self.pos_to_idx(r, c + 1)] = 0
            self.blank_pos = r, c + 1
            self.state = tuple(state)
        elif action == 2:
            state = list(self.state)
            state[self.pos_to_idx(r, c)] = self.state[self.pos_to_idx(r + 1, c)]
            state[self.pos_to_idx(r + 1, c)] = 0
            self.blank_pos = r + 1, c
            self.state = tuple(state)
        elif action == 3:
            state = list(self.state)
            state[self.pos_to_idx(r, c)] = self.state[self.pos_to_idx(r, c - 1)]
            state[self.pos_to_idx(r, c - 1)] = 0
            self.blank_pos = r, c - 1
            self.state = tuple(state)

    def reward(self):
        return 100000 if self.has_won() else -0.1

    def has_won(self):
        return self.state == self.goal_state

    def __repr__(self):
        return f'{self.state}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--episode', type=int, help='Number of episodes to train. Default: 30000.')
    parser.add_argument('-l', '--load', help='Load a pretrained Q-Matrix.', action='store_true')
    args = parser.parse_args()

    # Logger setup
    log_file_path = 'result.txt'
    try:
        os.remove(log_file_path)
    except OSError:
        pass
    log_file = logging.FileHandler(log_file_path)
    stdout = logging.StreamHandler(sys.stdout)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(log_file)
    logger.addHandler(stdout)

    if args.load:
        try:
            file_name = input('Specify file to load: ')
            with open(file_name, 'rb') as f:
                q = pickle.load(f)
            logger.debug(f'Successfully loaded \'{file_name}\'')
        except OSError:
            logger.debug('Failed to load Q-Matrix')
            logger.debug('Empty matrix employed\n')
            q = QLearning()
    else:
        q = QLearning()

    if args.episode is None:
        total_episode = 100000
    else:
        total_episode = args.episode

    if total_episode == 0:
        logger.debug(f'Skip training...')
    else:
        logger.debug(f'Start training {total_episode} episodes...')

    # For displaying average iteration count for last 100 episodes
    last_hundred_iters = deque()
    last_hundred_iter_sum = 0

    # Run episodes
    for episode in range(total_episode):
        # Reset puzzle
        p = Puzzle()
        i = 0
        score = 0

        # Initial exploit chance is 30%
        initial_exploit_chance = 0.3
        # It grows linearly reaching 80% at the last episode
        exploit_chance = initial_exploit_chance + (0.8 - initial_exploit_chance) * episode / total_episode

        while not p.has_won():
            i += 1
            next_states_actions = p.next_states_actions()

            # Exploit if possible and lucky
            if p.state in q.matrix and random.uniform(0, 1) <= exploit_chance:
                best_action = None
                best_next_p = None
                best_q = -math.inf
                for next_p, action in next_states_actions:
                    if best_q < q.matrix[p.state][action]:
                        best_q = q.matrix[p.state][action]
                        best_next_p, best_action = next_p, action
                next_p, action = best_next_p, best_action
            # Explore otherwise
            else:
                random.shuffle(next_states_actions)
                next_p, action = next_states_actions[0]
            reward = next_p.reward()
            score += reward
            q.update(p.state, action, reward, next_p.state)
            p = next_p

        # Housekeeping for last 100 episodes avg iterations
        if episode >= 100:
            last_hundred_iter_sum -= last_hundred_iters.popleft()
        last_hundred_iters.append(i)
        last_hundred_iter_sum += i
        avg = last_hundred_iter_sum / (100 if episode>=100 else episode + 1)

        logger.debug(f'Episode #{episode + 1} ended in {i} moves.  Score={score}.  Q-Matrix Size={len(q.matrix)}.  Avg moves of last 100 eps: {avg}')

    logger.debug('\nTraining Complete')
    logger.debug('Save trained Q-Matrix? (y/n)')
    if input() == 'y':
        try:
            file_name = input('Save as: ')
            with open(file_name, 'wb') as f:
                pickle.dump(q, f)
            logger.debug(f'Successfully saved Q-Matrix as \'{file_name}\'')
        except OSError:
            logger.debug('Failed to save Q-Matrix')

    # Solve puzzle in question
    logger.debug('\nSolving puzzle in question...\n')
    p = Puzzle()
    i = 0
    while not p.has_won():
        i += 1
        logger.debug(f'Move #{i}:')
        logger.debug(f'State before move: {p}')
        logger.debug(f'Q matrix for current state: {q.matrix[p.state]}')
        action = q.matrix[p.state].index(max(q.matrix[p.state]))
        logger.debug(f'Choosen action: {action}')
        p.move(action)
        logger.debug(f'State after move:  {p}\n')
    logger.debug(f'Solve with {i} moves.')


if __name__ == '__main__':
    main()



#!/usr/bin/env python
import sys

import click

from final import *

from env import TicTacToeEnv, agent_by_mark, check_game_status,\
    after_action_state, tomark, next_mark
"""
    state (tuple): Board status + mark

    agent_by_mark(agents, mark):
        recognizes an agent by the mark it posseses (either 'O' or 'X')

    check_game_status(board):
        returns 1 if 'O' wins,
        returns 2 if 'X' wins,
        returns 0 if draw,
        returns -1 if match still in progress

    after_action_state(state, action):
        returns tuple of two elements
            a 9 element tuple with 0, 1 and 2 representing blank, O, X respectively
            mark that comes next

    tomark:
        converts from symbol to int

    next_mark:
        changes between X and O
"""

HUMAN_MARK = 'O'
AI_MARK = 'X'


class HumanAgent(object):
    def __init__(self, mark):
        self.mark = mark

    def act(state, ava_actions):
        while True:
            uloc = input("Enter location[1-9], q for quit: ")
            if uloc.lower() == 'q':
                return None
            try:
                action = int(uloc)
                if action not in ava_actions:
                    raise ValueError()
                after_action_state(state, action - 1)
            except ValueError:
                print("Illegal location: '{}'".format(uloc))
            else:
                break

        return action


@click.command(help="Play minimax agent.")
@click.option('-n', '--show-number', is_flag=True, default=False,
              show_default=True, help="Show location number in the board.")
def play(show_number):

    env = TicTacToeEnv(show_number=show_number)
    agents = [HumanAgent(HUMAN_MARK)]
    episode = 0
    j = 0
    while True:

        state = env.reset()
        _, mark = state
        done = False
        env.render()
        i = 0
        if j == 0:
            Papa = Node(state, None, [1, 2, 3, 4, 5, 6, 7, 8, 9], 0)
            Papa.fill()
            j += 1
        action = Papa.maxAddress
        current = Papa.children[Papa.maxAddress]
        print("X's Turn")
        while not done:
            pre_action = action
            pre_current = current
            ava_actions = env.available_actions()
            if i % 2 == 0 and i != 0:
                print("X's Turn")
                print("Previous Action: ", pre_action)
                action, current = pre_current.reach_child(pre_action)
                print("Playing: ", action)
            elif i % 2 == 1:
                print("O's Turn")
                action = HumanAgent.act(state, ava_actions)

            i += 1
            if action is None:
                sys.exit()

            state, reward, done, info = env.step(action - 1)

            print('')
            env.render()
            if done:
                env.show_result(True, mark, reward)
                break
            else:
                _, _ = state
        mark = next_mark(mark)

        episode += 1


if __name__ == '__main__':
    play()

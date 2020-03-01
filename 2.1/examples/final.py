from env import check_game_status, tocode, next_mark


class Node():
    def __init__(self, state, parent, ava_actions, level):
        self.parent = parent
        self.ava_actions = ava_actions
        self.mark = state[1]
        self.board = state[0]
        self.value = 0
        self.level = level  # depth

    def fill(self):
        """
            Fills in the game tree

        """

        # Filling the leafs
        # For Papa
        if self.level == 0:
            self.children = {}
            print("Loading...\n10")
            for move in self.ava_actions:
                nstate, _ava_actions = self.acting(move)
                print(10 - move)
                self.children[move] = Node(nstate, self, _ava_actions, self.level + 1)
                self.children[move].fill()

        # For every other node
        elif self.level >= 1 and self.level <= 9:
            status = check_game_status(self.board)
            if status == 2:
                self.value = 10 - self.level
            elif status == 1:
                self.value = -10 + self.level
            elif status == 0:
                self.value = 0
            elif status == -1:
                self.children = {}
                for move in self.ava_actions:
                    nstate, _ava_actions = self.acting(move)
                    self.children[move] = Node(nstate, self, _ava_actions, self.level + 1)
                    self.children[move].fill()

        status = check_game_status(self.board)
        if status == -1:
            self.Max = self.children[self.ava_actions[0]].value
            self.maxAddress = self.ava_actions[0]
            self.Min = self.children[self.ava_actions[0]].value
            self.minAddress = self.ava_actions[0]
            for move in self.ava_actions:
                if self.Max < self.children[move].value:
                    self.Max = self.children[move].value
                    self.maxAddress = move

                if self.Min > self.children[move].value:
                    self.Min = self.children[move].value
                    self.minAddress = move

            if self.mark == 'O':
                self.value = self.Min
            if self.mark == 'X':
                self.value = self.Max

        if self.level == 0:
            print("Done!")

    def reach_child(self, move):
        return self.children[move].maxAddress, self.children[move].children[self.children[move].maxAddress]

    def acting(self, move):
        _ava_actions = self.ava_actions[:]
        _ava_actions.remove(move)
        nboard = list(self.board)
        nboard[move - 1] = tocode(self.mark)
        if self.mark == 'O':
            nstate = (nboard, 'X')
        elif self.mark == 'X':
            nstate = (nboard, 'O')

        return nstate, _ava_actions

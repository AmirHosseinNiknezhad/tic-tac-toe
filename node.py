import copy


class Node:
    def __init__(self, turn: int, position: list[list[int]]) -> None:
        self.side_to_move = turn
        self.position = position
        self.children: list[Node] = []
        self.winner: int | None = None
        self.is_drawn = False
        self.minimax_value = 0

    def to_str(self, starting_side: str) -> str:
        second_side = 'X' if starting_side == 'O' else 'O'
        num_to_side = {1: starting_side, 2: second_side}

        def transform(x: int):
            if x == 0:
                return '[ ]'
            else:
                return f'[{num_to_side[x]}]'
        transformed_position = [list(map(transform, row))
                                for row in self.position]
        board = '\n'.join([''.join(row) for row in transformed_position])
        return board

    def append_child(self, child: 'Node'):
        self.children.append(child)

    def check_winner_or_drawn(self):
        for i in range(3):
            # Check rows
            if self.position[i][0] == self.position[i][1] == self.position[i][2] and self.position[i][0] != 0:
                self.winner = self.position[i][0]
                return
            # Check columns
            if self.position[0][i] == self.position[1][i] == self.position[2][i] and self.position[0][i] != 0:
                self.winner = self.position[0][i]
                return
        # Check diagonals
        if self.position[0][0] == self.position[1][1] == self.position[2][2] and self.position[0][0] != 0:
            self.winner = self.position[0][0]
            return
        if self.position[0][2] == self.position[1][1] == self.position[2][0] and self.position[0][2] != 0:
            self.winner = self.position[0][2]
            return
        # Check for full board without winner
        if all(cell != 0 for row in self.position for cell in row):
            self.is_drawn = True

# TODO Avoid duplicates
    def create_children(self):
        if self.winner or self.is_drawn:
            return
        for i in range(3):
            for j in range(3):
                if self.position[i][j] == 0:
                    next_turn = 1 if self.side_to_move == 2 else 2
                    new_position = copy.deepcopy(self.position)
                    new_position[i][j] = self.side_to_move
                    child_node = Node(next_turn, new_position)
                    child_node.check_winner_or_drawn()
                    self.append_child(child_node)
                    child_node.create_children()
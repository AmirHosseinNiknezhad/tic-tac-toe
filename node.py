from copy import deepcopy
from json import dumps


class Node:
    nodes: dict[str, 'Node'] = {}

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

        def transform(x: int) -> str:
            return '[ ]' if x == 0 else f'[{num_to_side[x]}]'

        return '\n'.join([''.join(map(transform, row)) for row in self.position])

    def append_child(self, child: 'Node') -> None:
        self.children.append(child)

    def check_winner_or_drawn(self) -> None:
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

    def create_children_recursively(self) -> None:
        if self.winner or self.is_drawn:
            return
        for i in range(3):
            for j in range(3):
                if self.position[i][j] == 0:
                    self.position[i][j] = self.side_to_move
                    key = dumps(self.position)
                    if key in Node.nodes:
                        self.position[i][j] = 0
                        new_child = Node.nodes[key]
                        self.append_child(new_child)

                    else:
                        next_turn = 1 if self.side_to_move == 2 else 2
                        new_position = deepcopy(self.position)
                        self.position[i][j] = 0
                        new_child = Node(next_turn, new_position)
                        new_child.check_winner_or_drawn()
                        self.append_child(new_child)
                        Node.nodes[key] = new_child
                        new_child.create_children_recursively()

    def set_minimax_recursively(self, depth: int = 0) -> int:
        if self.winner:
            self.minimax_value = 10 - depth if self.winner == 1 else depth - 10
            return self.minimax_value
        if self.is_drawn:
            self.minimax_value = 0
            return self.minimax_value
        if self.side_to_move == 1:
            max_eval = -100
            for child in self.children:
                eval: int = child.set_minimax_recursively(depth + 1)
                max_eval = max(max_eval, eval)
            self.minimax_value = max_eval
            return max_eval
        else:
            min_eval = 100
            for child in self.children:
                eval = child.set_minimax_recursively(depth + 1)
                min_eval = min(min_eval, eval)
            self.minimax_value = min_eval
            return min_eval

    def get_best_move(self) -> 'Node':
        best_move = self
        if self.side_to_move == 1:
            best_value = -10
            for child in self.children:
                if child.minimax_value > best_value:
                    best_value = child.minimax_value
                    best_move = child
        else:
            best_value = 10
            for child in self.children:
                if child.minimax_value < best_value:
                    best_value = child.minimax_value
                    best_move = child
        return best_move

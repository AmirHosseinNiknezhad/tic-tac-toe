from enum import Enum, auto
from math import inf
from typing import ClassVar

WIN_SCORE = 100
DRAW_SCORE = 0


class GameState(Enum):
    IN_PROGRESS = auto()
    DRAW = auto()
    SIDE1_WIN = auto()
    SIDE2_WIN = auto()


class Node:
    nodes: ClassVar[dict[tuple[tuple[int, ...], ...], "Node"]] = {}

    def __init__(
        self, side_to_move: int, position: tuple[tuple[int, ...], ...]
    ) -> None:
        self.side_to_move = side_to_move
        self.position = position
        self.children: list[Node] = []
        self.state: GameState = Node.check_winner_or_drawn(position)
        self.minimax_value: int | None = None

    @staticmethod
    def position_with_move(
        position: tuple[tuple[int, ...], ...], i: int, j: int, side: int
    ) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(
                side if (row_idx == i and col_idx == j) else cell
                for col_idx, cell in enumerate(row)
            )
            for row_idx, row in enumerate(position)
        )

    @classmethod
    def from_parent(cls, parent: "Node", i: int, j: int) -> "Node":
        new_position = cls.position_with_move(
            parent.position, i, j, parent.side_to_move
        )
        next_side_to_move = 1 if parent.side_to_move == 2 else 2
        return cls(next_side_to_move, new_position)

    def to_str(self, starting_side: str) -> str:
        second_side = "X" if starting_side == "O" else "O"
        num_to_side = {1: starting_side, 2: second_side}

        def transform(x: int) -> str:
            return "[ ]" if x == 0 else f"[{num_to_side[x]}]"

        return "\n".join(["".join(map(transform, row)) for row in self.position])

    def append_child(self, child: "Node") -> None:
        self.children.append(child)

    @staticmethod
    def evaluate(
        position: tuple[tuple[int, ...], ...], side_to_move: int, depth: int = 0
    ) -> int:
        state = Node.check_winner_or_drawn(position)
        if state == GameState.SIDE1_WIN:
            return WIN_SCORE - depth
        if state == GameState.SIDE2_WIN:
            return depth - WIN_SCORE
        if state == GameState.DRAW:
            return DRAW_SCORE
        raise ValueError("Cannot evaluate non-terminal position")

    @staticmethod
    def check_winner_or_drawn(position: tuple[tuple[int, ...], ...]) -> GameState:
        for i in range(3):
            # Check rows
            if (
                position[i][0] == position[i][1] == position[i][2]
                and position[i][0] != 0
            ):
                return (
                    GameState.SIDE1_WIN if position[i][0] == 1 else GameState.SIDE2_WIN
                )
            # Check columns
            if (
                position[0][i] == position[1][i] == position[2][i]
                and position[0][i] != 0
            ):
                return (
                    GameState.SIDE1_WIN if position[0][i] == 1 else GameState.SIDE2_WIN
                )
        # Check diagonals
        if position[0][0] == position[1][1] == position[2][2] and position[0][0] != 0:
            return GameState.SIDE1_WIN if position[0][0] == 1 else GameState.SIDE2_WIN
        if position[0][2] == position[1][1] == position[2][0] and position[0][2] != 0:
            return GameState.SIDE1_WIN if position[0][2] == 1 else GameState.SIDE2_WIN
        # Check for full board without winner
        if all(cell != 0 for row in position for cell in row):
            return GameState.DRAW
        return GameState.IN_PROGRESS

    def create_children_recursively(self) -> None:
        if self.state != GameState.IN_PROGRESS:
            return
        for i in range(3):
            for j in range(3):
                if self.position[i][j] == 0:
                    new_child = Node.from_parent(self, i, j)
                    key = new_child.position
                    if key in Node.nodes:
                        new_child = Node.nodes[key]
                        self.append_child(new_child)
                    else:
                        self.append_child(new_child)
                        Node.nodes[key] = new_child
                        new_child.create_children_recursively()

    def set_minimax_recursively(self, depth: int = 0) -> int:
        if self.state != GameState.IN_PROGRESS:
            self.minimax_value = Node.evaluate(self.position, self.side_to_move, depth)
            return self.minimax_value
        if self.side_to_move == 1:
            max_eval = -inf
            for child in self.children:
                child_val: int = child.set_minimax_recursively(depth + 1)
                if child_val > max_eval:
                    max_eval = child_val
            self.minimax_value = int(max_eval)
            return self.minimax_value
        else:
            min_eval = inf
            for child in self.children:
                child_val = child.set_minimax_recursively(depth + 1)
                if child_val < min_eval:
                    min_eval = child_val
            self.minimax_value = int(min_eval)
            return self.minimax_value

    def get_best_moves(self) -> list["Node"]:
        if self.side_to_move == 1:
            best_value = -WIN_SCORE
            best_moves: list["Node"] = []
            for child in self.children:
                if child.minimax_value is None:
                    raise TypeError("Expected evaluated minimax_value on child node")
                if child.minimax_value > best_value:
                    best_value = child.minimax_value
                    best_moves = [child]
                elif child.minimax_value == best_value:
                    best_moves.append(child)
        else:
            best_value = WIN_SCORE
            best_moves = []
            for child in self.children:
                if child.minimax_value is None:
                    raise TypeError("Expected evaluated minimax_value on child node")
                if child.minimax_value < best_value:
                    best_value = child.minimax_value
                    best_moves = [child]
                elif child.minimax_value == best_value:
                    best_moves.append(child)

        return best_moves

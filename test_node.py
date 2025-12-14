import pytest

from node import DRAW_SCORE, GameState, Node, WIN_SCORE


class TestCheckWinnerOrDrawn:
    def test_empty_board(self):
        position = tuple(tuple(0 for _ in range(3)) for _ in range(3))
        assert Node.check_winner_or_drawn(position) == GameState.IN_PROGRESS

    def test_row_win_side1(self):
        position = (
            (1, 1, 1),
            (0, 0, 0),
            (0, 0, 0),
        )
        assert Node.check_winner_or_drawn(position) == GameState.SIDE1_WIN

    def test_row_win_side2(self):
        position = (
            (2, 2, 2),
            (0, 0, 0),
            (0, 0, 0),
        )
        assert Node.check_winner_or_drawn(position) == GameState.SIDE2_WIN

    def test_column_win_side1(self):
        position = (
            (1, 0, 0),
            (1, 0, 0),
            (1, 0, 0),
        )
        assert Node.check_winner_or_drawn(position) == GameState.SIDE1_WIN

    def test_diagonal_win_side1(self):
        position = (
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1),
        )
        assert Node.check_winner_or_drawn(position) == GameState.SIDE1_WIN

    def test_anti_diagonal_win_side2(self):
        position = (
            (0, 0, 2),
            (0, 2, 0),
            (2, 0, 0),
        )
        assert Node.check_winner_or_drawn(position) == GameState.SIDE2_WIN

    def test_draw(self):
        position = (
            (1, 2, 1),
            (2, 2, 1),
            (2, 1, 2),
        )
        assert Node.check_winner_or_drawn(position) == GameState.DRAW

    def test_in_progress_partial(self):
        position = (
            (1, 2, 0),
            (2, 1, 0),
            (0, 0, 0),
        )
        assert Node.check_winner_or_drawn(position) == GameState.IN_PROGRESS


class TestPositionWithMove:
    def test_apply_move_to_empty(self):
        position = tuple(tuple(0 for _ in range(3)) for _ in range(3))
        new_position = Node.position_with_move(position, 0, 0, 1)
        assert new_position[0][0] == 1
        assert new_position[0][1] == 0
        assert new_position[1][0] == 0

    def test_apply_move_middle(self):
        position = tuple(tuple(0 for _ in range(3)) for _ in range(3))
        new_position = Node.position_with_move(position, 1, 1, 2)
        assert new_position[1][1] == 2
        assert all(
            new_position[i][j] == 0
            for i in range(3)
            for j in range(3)
            if (i, j) != (1, 1)
        )

    def test_immutability(self):
        position = tuple(tuple(0 for _ in range(3)) for _ in range(3))
        original_id = id(position)
        new_position = Node.position_with_move(position, 0, 0, 1)
        assert id(position) == original_id
        assert position != new_position


class TestEvaluate:
    def test_evaluate_side1_win(self):
        position = (
            (1, 1, 1),
            (0, 0, 0),
            (0, 0, 0),
        )
        score = Node.evaluate(position, side_to_move=1, depth=0)
        assert score == WIN_SCORE

    def test_evaluate_side1_win_with_depth(self):
        position = (
            (1, 1, 1),
            (0, 0, 0),
            (0, 0, 0),
        )
        score = Node.evaluate(position, side_to_move=1, depth=3)
        assert score == WIN_SCORE - 3

    def test_evaluate_side2_win(self):
        position = (
            (2, 2, 2),
            (0, 0, 0),
            (0, 0, 0),
        )
        score = Node.evaluate(position, side_to_move=2, depth=0)
        assert score == -WIN_SCORE

    def test_evaluate_side2_win_with_depth(self):
        position = (
            (2, 2, 2),
            (0, 0, 0),
            (0, 0, 0),
        )
        score = Node.evaluate(position, side_to_move=2, depth=5)
        assert score == 5 - WIN_SCORE

    def test_evaluate_draw(self):
        position = (
            (1, 2, 1),
            (2, 2, 1),
            (2, 1, 2),
        )
        score = Node.evaluate(position, side_to_move=1, depth=0)
        assert score == DRAW_SCORE

    def test_evaluate_non_terminal_raises(self):
        position = tuple(tuple(0 for _ in range(3)) for _ in range(3))
        with pytest.raises(ValueError, match="Cannot evaluate non-terminal"):
            Node.evaluate(position, side_to_move=1, depth=0)


class TestFromParent:
    def test_from_parent_applies_move(self):
        parent = Node(1, tuple(tuple(0 for _ in range(3)) for _ in range(3)))
        child = Node.from_parent(parent, 0, 0)
        assert child.position[0][0] == 1
        assert child.side_to_move == 2

    def test_from_parent_switches_turn(self):
        parent = Node(1, tuple(tuple(0 for _ in range(3)) for _ in range(3)))
        child = Node.from_parent(parent, 1, 1)
        assert child.side_to_move == 2
        grandchild = Node.from_parent(child, 0, 0)
        assert grandchild.side_to_move == 1


class TestSmokeTests:
    def test_node_creation(self):
        position = tuple(tuple(0 for _ in range(3)) for _ in range(3))
        node = Node(1, position)
        assert node.side_to_move == 1
        assert node.state == GameState.IN_PROGRESS
        assert node.minimax_value is None

    def test_node_creation_winning_position(self):
        position = (
            (1, 1, 1),
            (0, 0, 0),
            (0, 0, 0),
        )
        node = Node(1, position)
        assert node.state == GameState.SIDE1_WIN

    def test_minimax_evaluation_smoke(self):
        position = (
            (1, 1, 0),
            (2, 2, 0),
            (0, 0, 0),
        )
        node = Node(1, position)
        node.create_children_recursively()
        node.set_minimax_recursively()
        assert node.minimax_value is not None
        assert node.minimax_value > 0

    def test_get_best_move_smoke(self):
        position = tuple(tuple(0 for _ in range(3)) for _ in range(3))
        node = Node(1, position)
        for i, j in [(0, 0), (1, 1), (2, 2)]:
            child = Node.from_parent(node, i, j)
            node.append_child(child)
        node.children[0].minimax_value = 10
        node.children[1].minimax_value = 20
        node.children[2].minimax_value = 5
        node.minimax_value = 20
        best = node.get_best_move()
        assert best.minimax_value == 20

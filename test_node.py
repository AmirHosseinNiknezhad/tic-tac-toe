import pytest

from node import DRAW_SCORE, WIN_SCORE, GameState, Node

EMPTY_POSITION = (
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
)


def test_position_with_move_returns_new_position():
    position = EMPTY_POSITION
    new_position = Node.position_with_move(position, 1, 2, 1)

    assert position == EMPTY_POSITION
    for r in range(3):
        for c in range(3):
            if r == 1 and c == 2:
                assert new_position[r][c] == 1
            else:
                assert new_position[r][c] == 0


def test_from_parent_switches_side_and_places_piece():
    parent = Node(side_to_move=1, position=EMPTY_POSITION)
    child = Node.from_parent(parent, 0, 1)

    assert child.side_to_move == 2
    assert child.position[0][1] == 1


def test_check_winner_or_drawn_detects_states():
    row_win = (
        (1, 1, 1),
        (0, 2, 0),
        (0, 0, 2),
    )
    col_win = (
        (2, 1, 0),
        (2, 1, 0),
        (2, 0, 1),
    )
    diag_win = (
        (1, 2, 0),
        (0, 1, 2),
        (0, 0, 1),
    )
    draw = (
        (1, 2, 1),
        (1, 2, 2),
        (2, 1, 1),
    )
    in_progress = (
        (1, 0, 0),
        (0, 2, 0),
        (0, 0, 0),
    )

    assert Node.check_winner_or_drawn(row_win) == GameState.SIDE1_WIN
    assert Node.check_winner_or_drawn(col_win) == GameState.SIDE2_WIN
    assert Node.check_winner_or_drawn(diag_win) == GameState.SIDE1_WIN
    assert Node.check_winner_or_drawn(draw) == GameState.DRAW
    assert Node.check_winner_or_drawn(in_progress) == GameState.IN_PROGRESS


def test_evaluate_depth_adjusts_scores():
    side1_win = (
        (1, 1, 1),
        (0, 2, 0),
        (0, 0, 2),
    )
    side2_win = (
        (2, 2, 2),
        (1, 1, 0),
        (0, 0, 1),
    )
    draw = (
        (1, 2, 1),
        (1, 2, 2),
        (2, 1, 1),
    )

    assert Node.evaluate(side1_win, depth=2) == WIN_SCORE - 2
    assert Node.evaluate(side2_win, depth=3) == 3 - WIN_SCORE
    assert Node.evaluate(draw, depth=5) == DRAW_SCORE


def test_evaluate_raises_on_non_terminal():
    with pytest.raises(ValueError):
        Node.evaluate(EMPTY_POSITION)


def test_create_children_recursively_single_move_left():
    position = (
        (1, 2, 1),
        (1, 2, 2),
        (2, 1, 0),
    )
    node = Node(side_to_move=1, position=position)
    node.create_children_recursively()
    assert len(node.children) == 1
    child = node.children[0]
    assert child.state == GameState.DRAW

    value = node.set_minimax_recursively()
    assert value == DRAW_SCORE
    assert node.minimax_value == DRAW_SCORE


def test_get_best_moves_prefers_max_for_side1():
    parent = Node(side_to_move=1, position=EMPTY_POSITION)
    child_a = Node(
        side_to_move=2, position=Node.position_with_move(EMPTY_POSITION, 0, 0, 1)
    )
    child_b = Node(
        side_to_move=2, position=Node.position_with_move(EMPTY_POSITION, 0, 1, 1)
    )
    child_c = Node(
        side_to_move=2, position=Node.position_with_move(EMPTY_POSITION, 0, 2, 1)
    )
    child_a.minimax_value = 3
    child_b.minimax_value = 5
    child_c.minimax_value = 5
    parent.children = [child_a, child_b, child_c]

    best = parent.get_best_moves()
    assert best == [child_b, child_c]


def test_get_best_moves_prefers_min_for_side2():
    parent = Node(side_to_move=2, position=EMPTY_POSITION)
    child_a = Node(
        side_to_move=1, position=Node.position_with_move(EMPTY_POSITION, 0, 0, 2)
    )
    child_b = Node(
        side_to_move=1, position=Node.position_with_move(EMPTY_POSITION, 0, 1, 2)
    )
    child_c = Node(
        side_to_move=1, position=Node.position_with_move(EMPTY_POSITION, 0, 2, 2)
    )
    child_a.minimax_value = -2
    child_b.minimax_value = -5
    child_c.minimax_value = -5
    parent.children = [child_a, child_b, child_c]

    best = parent.get_best_moves()
    assert best == [child_b, child_c]


def test_get_best_moves_requires_minimax_values():
    parent = Node(side_to_move=1, position=EMPTY_POSITION)
    child = Node(
        side_to_move=2, position=Node.position_with_move(EMPTY_POSITION, 0, 0, 1)
    )
    parent.children = [child]

    with pytest.raises(TypeError):
        parent.get_best_moves()

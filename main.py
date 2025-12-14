import argparse
from os import path
from pickle import dump, load
from random import choice
from time import sleep

from node import GameState, Node


def main() -> None:
    parser = argparse.ArgumentParser(description="Play Tic-Tac-Toe against AI")
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Rebuild the game tree from scratch instead of using cache",
    )
    args = parser.parse_args()

    print("🎮 Welcome to Tic-Tac-Toe!\n")
    # Ask the user which side they want to play
    decision = get_yes_or_no("Would you like to play as X?", random=True)
    human_side = "X" if decision == "yes" else "O"
    computer_side = "X" if human_side == "O" else "O"
    print(f"✓ You are {human_side} — Computer is {computer_side}\n")
    # Ask the user if they want to go first
    decision = get_yes_or_no("Would you like to go first?", random=True)
    starting_player = "human" if decision == "yes" else "computer"
    print(f"✓ {'You' if starting_player == 'human' else 'Computer'} will start\n")
    # Ask if the user wants to see the evaluation of the current and possible positions
    decision = get_yes_or_no("Show position evaluations?", default="no")
    show_eval = decision == "yes"
    if show_eval:
        print(
            "📊 Evaluations enabled\n(Positive = first player advantage, Negative = second player advantage)\n"
        )
    else:
        print("📊 Evaluations hidden\n")

    # Either load game tree from cache or create and cache it
    root: Node | None = None
    if not args.fresh:
        root = load_cached_tree()
    if not root:
        print("🌳 Building game tree", end="", flush=True)
        root = build_tree()
        cache_tree(root)
        print(" ✓ Done!\n")
    # Either set an empty board as the starting position for the human or select a random first move for the AI
    current_node: Node = root if starting_player == "human" else choice(root.children)
    starting_side = human_side if starting_player == "human" else computer_side
    # Game loop
    while True:
        print(current_node.to_str(starting_side))
        if show_eval:
            print(f"Eval: {current_node.minimax_value}")
        # End the game if the board is full or if a player has won
        if current_node.state in (GameState.SIDE1_WIN, GameState.SIDE2_WIN):
            if GameState.SIDE1_WIN and starting_player == "computer" or GameState.SIDE2_WIN and starting_player == "human":
                print("\n🤖 Computer wins! Well played.\n")
            else:
                print("\n🎉 You win! Congratulations!\n")
            break
        if current_node.state == GameState.DRAW:
            print("\n🤝 It's a draw!\n")
            break
        # Determine the side to play and either have the AI make the move or prompt the user for a move
        print()
        if (current_node.side_to_move == 1 and starting_player == "computer") or (
            current_node.side_to_move == 2 and starting_player == "human"
        ):
            simulate_thinking("🤖 Computer is thinking")
            print("\n")
            current_node = current_node.get_best_move()
        # Make the move for the user if it's forced
        elif len(current_node.children) == 1:
            simulate_thinking("⚡ Your move is forced")
            print("\n")
            current_node = current_node.get_best_move()
        # Get a move from the user
        else:
            i, j = prompt_user_move(current_node, show_eval)
            new_position = Node.position_with_move(
                current_node.position, i, j, current_node.side_to_move
            )
            for child in current_node.children:
                if child.position == new_position:
                    current_node = child
                    break
            print()


def cache_tree(root: Node) -> None:
    with open("tree-cache.pkl", "wb") as file:
        dump(root, file)


def load_cached_tree() -> None | Node:
    if path.exists("tree-cache.pkl"):
        with open("tree-cache.pkl", mode="rb") as file:
            return load(file)
    return None


def build_tree() -> Node:
    initial_position = tuple(tuple(0 for _ in range(3)) for _ in range(3))
    root = Node(turn=1, position=initial_position)
    Node.nodes[initial_position] = root
    root.create_children_recursively()
    root.set_minimax_recursively()
    return root


def prompt_user_move(
    current_node: Node,
    show_eval: bool,
) -> tuple[int, int]:
    number_to_move = {
        1: (0, 0),
        2: (0, 1),
        3: (0, 2),
        4: (1, 0),
        5: (1, 1),
        6: (1, 2),
        7: (2, 0),
        8: (2, 1),
        9: (2, 2),
    }
    print("👤 Your turn! Enter a cell number (1-9) or press Enter for a random move.")
    available_moves = [
        key
        for key in number_to_move
        if current_node.position[number_to_move[key][0]][number_to_move[key][1]] == 0
    ]
    available_moves_with_eval = None
    if show_eval:
        move_to_minimax: dict[int, int] = {}
        for child in current_node.children:
            for move in available_moves:
                if (
                    child.position[number_to_move[move][0]][number_to_move[move][1]]
                    == current_node.side_to_move
                ):
                    if child.minimax_value is None:
                        raise TypeError(
                            "Expected evaluated minimax_value on child node"
                        )
                    move_to_minimax[move] = child.minimax_value
                    break
        # Sort moves by value: descending for side 1 (higher is better), ascending for side 2 (lower is better)
        if current_node.side_to_move == 1:
            available_moves_with_eval = dict(
                sorted(move_to_minimax.items(), key=lambda x: x[1], reverse=True)
            )
        else:
            available_moves_with_eval = dict(
                sorted(move_to_minimax.items(), key=lambda x: x[1])
            )
    while True:
        if show_eval:
            print(f"Available: {available_moves_with_eval} ", end="")
        else:
            print(f"Available: {available_moves} ", end="")
        try:
            move = input("> ").strip()
            if move == "":
                move = choice(available_moves)
                print(f"Random choice: {move}\n")
                i, j = number_to_move[move]
                break
            else:
                if not move.isdigit():
                    raise ValueError("Please enter a valid number.")
            move = int(move)
            if move not in number_to_move:
                raise ValueError("Cell number must be between 1 and 9.")
            i, j = number_to_move[move]
            if current_node.position[i][j] != 0:
                raise ValueError("That cell is already occupied.")
            break
        except ValueError as e:
            print(f"❌ {e}")
    return i, j


def get_yes_or_no(prompt: str, random: bool = False, default: str | None = None) -> str:
    prompt = prompt + " "
    if random:
        prompt += "[Y/N — Enter for random] "
    elif default:
        prompt += f"[Y/N — Enter for {default}] "
    else:
        prompt += "[Y/N] "
    while True:
        try:
            decision = input(prompt).lower().strip()
            if decision in ["n", "no"]:
                return "no"
            elif decision in ["y", "yes"]:
                return "yes"
            elif decision == "":
                if random:
                    return choice(["yes", "no"])
                if default:
                    return default
                else:
                    raise ValueError("Please enter Y or N.")
            else:
                raise ValueError("Please enter Y, N, or press Enter.")
        except ValueError as e:
            print(f"❌ {e}")


def simulate_thinking(message: str) -> None:
    print(message, end="", flush=True)
    for _ in range(3):
        print(".", end="", flush=True)
        sleep(0.5)
    print("\n")


if __name__ == "__main__":
    main()

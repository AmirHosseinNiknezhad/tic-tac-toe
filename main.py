import copy
import os
import random
import pickle
import time
from node import Node
# TODO organize code


def minimax(node: Node, depth: int = 0) -> int:
    if node.winner:
        node.minimax_value = 10 - depth if node.winner == 1 else depth - 10
        return node.minimax_value
    if node.is_drawn:
        node.minimax_value = 0
        return node.minimax_value
    if node.side_to_move == 1:
        max_eval = -100
        for child in node.children:
            eval = minimax(child, depth + 1)
            max_eval = max(max_eval, eval)
        node.minimax_value = max_eval
        return max_eval
    else:
        min_eval = 100
        for child in node.children:
            eval = minimax(child, depth + 1)
            min_eval = min(min_eval, eval)
        node.minimax_value = min_eval
        return min_eval


def get_best_move(current_node: Node) -> Node:
    best_move = current_node
    if current_node.side_to_move == 1:
        best_value = -10
        for child in current_node.children:
            if child.minimax_value > best_value:
                best_value = child.minimax_value
                best_move = child
    else:
        best_value = 10
        for child in current_node.children:
            if child.minimax_value < best_value:
                best_value = child.minimax_value
                best_move = child
    return best_move


def cache_tree(root: Node, file_name: str = 'tree.pkl'):
    # Cache the tree to a file.
    with open(file_name, 'wb') as file:
        pickle.dump(root, file)


def load_cached_tree(file_name: str = 'tree.pkl'):
    # Load cached tree from a file.
    if os.path.exists(file_name):
        with open(file_name, 'rb') as file:
            return pickle.load(file)
    return None


# Game logic
os.system('clear')
print('Welcome to Tic-Tac-Toe!')

while True:
    try:
        decision = input(
            'Do you want to go first? [Y/N] (Press Enter for a random choice) ').lower()
        if decision == 'no' or decision == 'n':
            starting_player = 'computer'
        elif decision == 'yes' or decision == 'y':
            starting_player = 'human'
        elif decision == '':
            starting_player = random.choice(['human', 'computer'])
        else:
            raise ValueError('Please input y or n or simply press Enter')
        break
    except ValueError as e:
        print(e)
print(f'{'Computer' if starting_player == 'computer' else 'You'} will begin')

# TODO easy mode to explore

while True:
    try:
        decision = input(
            'Do you want to be X or O? [X/O] (Press Enter for a random choice)').lower()
        if decision == 'x':
            human_side = 'X'
        elif decision == 'o':
            human_side = 'O'
        elif decision == '':
            human_side = random.choice(['X', 'O'])
        else:
            raise ValueError("Please input X or O, or simply press Enter")
        break
    except ValueError as e:
        print(e)
computer_side = 'X' if human_side == 'O' else 'O'
print(f'You play {human_side} and the computer plays {computer_side}')

starting_position = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]
number_to_move = {
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (2, 0),
    8: (2, 1),
    9: (2, 2)
}
root = load_cached_tree()
if not root:
    root = Node(1, starting_position)
    root.create_children()
    minimax(root)
    cache_tree(root)

current_node: Node = root
if starting_player == 'computer':
    rand = random.choice(list(range(1, 10)))
    i, j = number_to_move[rand]
    starting_position[i][j] = 1
    for child in root.children:
        if child.position == starting_position:
            current_node = child
            break

starting_side = human_side if starting_player == 'human' else computer_side
# Game loop
print()
while True:
    print(current_node.to_str(starting_side))
    print()
    if current_node.winner:
        if (current_node.winner == 1 and starting_player == 'computer') or (current_node.winner == 2 and starting_player == 'human'):
            print('The computer wins ;(')
        else:
            print('You win!!!')
        break
    if current_node.is_drawn:
        print("The game is a draw!")
        break
    if (current_node.side_to_move == 1 and starting_player == 'computer') or (current_node.side_to_move == 2 and starting_player == 'human'):
        print("Computer's move:")
        time.sleep(1.5)
        current_node = get_best_move(current_node)
    else:
        # TODO make forced move
        while True:
            try:
                print(
                    "It's your turn. Input the number of the cell you want to choose.", end=' ')
                print("Available moves:", [
                      key for key in number_to_move if current_node.position[number_to_move[key][0]][number_to_move[key][1]] == 0], end=' ')
                move = input()
                if move == '':
                    raise ValueError("You didn't enter a number")
                if int(move) not in number_to_move:
                    raise ValueError("Invalid input")
                i, j = number_to_move[int(move)]
                if current_node.position[i][j] != 0:
                    raise ValueError("Cell already occupied")
                break
            except ValueError as e:
                print(e)
        new_position = copy.deepcopy(current_node.position)
        new_position[i][j] = current_node.side_to_move
        for child in current_node.children:
            if child.position == new_position:
                current_node = child
                break

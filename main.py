from copy import deepcopy
from os import system, path
from random import choice
from pickle import dump, load
from time import sleep
from node import Node


def main() -> None:
    system('clear')
    print('Let\'s play to Tic-Tac-Toe!')

    # Ask the user which side they want to play
    decision = get_yes_or_no('Do you want to play X?', True)
    human_side = 'X' if decision == 'yes' else 'O'
    computer_side = 'X' if human_side == 'O' else 'O'

    # Ask the user if they want to go first
    decision = get_yes_or_no(prompt='Do you want to go first?', random=True)
    starting_player = 'human' if decision == 'yes' else 'computer'

    # Ask if the user wants to see the evaluation of the current and  possible positions
    decision = get_yes_or_no(
        prompt='Do you want to see the evaluation of the positions?', default='no')
    show_eval = True if decision == 'yes' else False

    # Some necessary variables
    starting_side = human_side if starting_player == 'human' else computer_side
    number_to_move = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (
        1, 0), 5: (1, 1), 6: (1, 2), 7: (2, 0), 8: (2, 1), 9: (2, 2)}

    print(f'You play {human_side} and the computer plays {computer_side}')
    print(f'{'You' if starting_player == 'human' else 'The computer'} will begin')
    if show_eval:
        print('Evaluations will be shown.\nA positive number means a win for the side which started the game and a negative number a win for the second player. A bigger number signifies a faster win.')
    print()

    # Either load game tree from cache or create and cache it
    root: Node | None = load_cached_tree()
    if not root:
        starting_position = [[0] * 3 for _ in range(3)]
        root = Node(1, starting_position)
        root.create_children_recursively()
        root.set_minimax_recursively()
        cache_tree(root)

    # Either set an empty board as the starting position for the human or select a random first move for the AI
    current_node: Node = root if starting_player == 'human' else choice(
        root.children)

    # Game loop
    while True:
        print(current_node.to_str(starting_side))
        if show_eval:
            print(f'Eval: {current_node.minimax_value}')

        # End the game if the board is full or if a player has won
        if current_node.winner:
            if (current_node.winner == 1 and starting_player == 'computer') or (current_node.winner == 2 and starting_player == 'human'):
                print()
                print('The computer wins')
            else:
                print()
                print('You win!')
            break
        if current_node.is_drawn:
            print()
            print('The game is a draw')
            break

        # Determine the side to play and either have the AI make the move or prompt the user for a move
        print()
        if (current_node.side_to_move == 1 and starting_player == 'computer') or (current_node.side_to_move == 2 and starting_player == 'human'):
            print('Computer\'s move', end='')
            for _ in range(3):
                print('.', end='')
                sleep(1)
            print()
            current_node = current_node.get_best_move()
            print()

        # Make the move for the user if it's forced
        elif sum(cell == 0 for row in current_node.position for cell in row) == 1:
            print('Your last move is forced', end='')
            for _ in range(3):
                print('.', end='')
                sleep(1)
            current_node = current_node.children[0]
        # Get a move from the user
        else:
            while True:
                try:
                    print(
                        'It\'s your turn. Input the number of the cell you want to choose.', end=' ')
                    available_moves = [
                        key for key in number_to_move if current_node.position[number_to_move[key][0]][number_to_move[key][1]] == 0]
                    if show_eval:
                        move_to_minimax: dict[int, int] = {}
                        for child in current_node.children:
                            for move in available_moves:
                                if child.position[number_to_move[move][0]][number_to_move[move][1]] == current_node.side_to_move:
                                    move_to_minimax[move] = child.minimax_value
                                    break
                        print('Available moves and their evaluations:',
                              move_to_minimax, end=' ')
                    else:
                        print('Available moves:', available_moves, end=' ')
                    move = input()
                    if move == '':
                        raise ValueError('You didn\'t enter a number')
                    if int(move) not in number_to_move:
                        raise ValueError('Invalid input')
                    i, j = number_to_move[int(move)]
                    if current_node.position[i][j] != 0:
                        raise ValueError('Cell already occupied')
                    break
                except ValueError as e:
                    print(e)
            new_position = deepcopy(current_node.position)
            new_position[i][j] = current_node.side_to_move
            for child in current_node.children:
                if child.position == new_position:
                    current_node = child
                    break
            print()


def cache_tree(root: Node) -> None:
    with open('tree-cache.pkl', 'wb') as file:
        dump(root, file)


def load_cached_tree() -> None | Node:
    if path.exists(path='tree-cache.pkl'):
        with open('tree-cache.pkl', mode='rb') as file:
            return load(file)
    return None


def get_yes_or_no(prompt: str, random: bool = False, default: str | None = None) -> str:
    prompt = prompt + ' [Y/N] '
    if random:
        prompt = prompt + '(Press Enter for a random choice) '
    elif default:
        prompt = prompt + f'(Press Enter to chose {default}) '
    while True:
        try:
            decision = input(prompt).lower()
            if decision in ['n', 'no']:
                return 'no'
            elif decision in ['y', 'yes']:
                return 'yes'
            elif decision == '':
                if random:
                    return choice(['yes', 'no'])
                if default:
                    return default
                else:
                    raise ValueError("Please input Either Y or N")
            else:
                raise ValueError(f'Please input Y or N {
                                 'or press Enter' if random else ''} {f'or press Enter to choose {default}' if default else ''}')
        except ValueError as e:
            print(e)


if __name__ == '__main__':
    main()

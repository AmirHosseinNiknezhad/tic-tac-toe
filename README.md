# Tic-Tac-Toe with Perfect AI

A command-line Tic-Tac-Toe game featuring an unbeatable AI opponent that uses the minimax algorithm with complete game tree evaluation.

## Features

- 🎮 **Interactive CLI** - Clean, emoji-enhanced user interface
- 🤖 **Perfect AI** - Uses minimax algorithm with full game tree (never loses)
- 📊 **Position Analysis** - Optional display of board evaluations and move scores
- ⚡ **Smart Caching** - Game tree is computed once and cached for instant subsequent plays
- ✅ **Input Validation** - Robust error handling and user-friendly prompts
- 🎲 **Flexible Setup** - Choose your side (X or O), who goes first, and whether to see evaluations

## How It Works

The AI builds a complete game tree of all ~5,500 possible tic-tac-toe positions on first run. Each position is evaluated using the minimax algorithm:

- **Positive scores** favor the first player (X)
- **Negative scores** favor the second player (O)
- **Depth-adjusted scoring** makes the AI prefer faster wins and slower losses

The tree is cached to disk with automatic invalidation when the game logic changes.

## Installation

### Prerequisites
- Python 3.14+ (or adjust `.python-version` for your version)

### Option 1: Using UV (Recommended)
```bash
git clone https://github.com/yourusername/tic-tac-toe.git
cd tic-tac-toe
uv run main.py
```

### Option 2: Using Standard Python
```bash
git clone https://github.com/yourusername/tic-tac-toe.git
cd tic-tac-toe
python main.py
```

## Usage

### Basic Play
```bash
python main.py
```

On first run, the game builds and caches the complete game tree (takes a few seconds). Subsequent runs start instantly.

### Rebuild Game Tree
To force a rebuild of the cached game tree:
```bash
python main.py --fresh
```

### Gameplay Example
```
🎮 Welcome to Tic-Tac-Toe!

Would you like to play as X? [Y/N — Enter for random] > y
✓ You are X — Computer is O

Would you like to go first? [Y/N — Enter for random] > y
✓ You will start

Show position evaluations? [Y/N — Enter for no] > y
📊 Evaluations enabled
(Positive = first player advantage, Negative = second player advantage)

🌳 Building game tree... ✓ Done!

[ ][ ][ ]
[ ][ ][ ]
[ ][ ][ ]
Eval: 0

👤 Your turn! Enter a cell number (1-9) or press Enter for a random move.
Available: {5: 0, 1: 0, 3: 0, 7: 0, 9: 0, 2: 0, 4: 0, 6: 0, 8: 0} > 5
```

### Cell Numbering
```
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
```

## Development

### Running Tests
```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest test_node.py -v
```

### Project Structure
```
tic-tac-toe/
├── main.py          # Game loop, UI, and user interaction
├── node.py          # Game tree node, minimax algorithm, win detection
├── test_node.py     # Tests for game logic
├── test_cache.py    # Tests for caching system
├── tree-cache.pkl   # Cached game tree (auto-generated)
└── README.md        # This file
```

## Technical Details

### Algorithm
- **Minimax with complete tree**: All possible game states are pre-computed
- **Transposition table**: Identical board positions are shared (memory optimization)
- **Depth-adjusted evaluation**: Wins in fewer moves score higher

### Performance
- **Initial build**: ~1 second to generate complete game tree
- **Tree size**: ~5,500 unique positions (reduced via symmetry sharing)
- **Cache file**: ~1-2 MB
- **Move selection**: Instant (pre-computed)

### Cache Versioning
The cache automatically invalidates when `node.py` changes. The system hashes the file content to detect modifications to game logic, ensuring the cache never becomes stale.

## Rules

- Players alternate placing their mark (X or O) on a 3×3 grid
- First player to get three marks in a row (horizontal, vertical, or diagonal) wins
- If all nine spaces are filled with no winner, the game is a draw
- The AI plays perfectly: it will always win or draw, never lose

## Contributing

This is a learning project demonstrating:
- Minimax algorithm implementation
- Game tree data structures
- CLI design patterns
- Comprehensive testing with pytest

Feel free to fork and experiment!

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built to demonstrate perfect play in a solved game using classic AI techniques.
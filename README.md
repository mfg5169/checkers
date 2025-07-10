# Checkers AI with Minimax Algorithm

A Python implementation of the classic Checkers game featuring an intelligent AI opponent using the Minimax algorithm with Alpha-Beta pruning. This project demonstrates advanced game theory concepts and provides a complete, playable Checkers experience with a graphical interface.

## 🎮 Features

- **Complete Checkers Game**: Full implementation of standard Checkers rules
- **Intelligent AI**: AI opponent using Minimax algorithm with Alpha-Beta pruning
- **Graphical Interface**: Pygame-based visual interface with smooth animations
- **Multi-hop Captures**: Support for complex capture sequences
- **King Promotion**: Automatic promotion to king pieces
- **Move Validation**: Comprehensive move validation and highlighting
- **Test Suite**: Extensive unit tests for AI evaluation and move generation

## 🏗️ Architecture

### Core Components

- **`main.py`**: Entry point and game loop management
- **`game.py`**: Game logic, move generation, and state management
- **`board.py`**: Board representation and piece management
- **`piece.py`**: Individual piece behavior and properties
- **`ai.py`**: AI implementation with Minimax and evaluation functions
- **`display.py`**: Pygame-based graphical rendering
- **`constants.py`**: Game constants and configuration
- **`board_configs.py`**: Predefined board configurations for testing

### Key Algorithms

#### Minimax with Alpha-Beta Pruning
The AI uses a depth-limited Minimax search with Alpha-Beta pruning to find optimal moves:

```python
def minimax_alpha_beta(board, depth, alpha, beta, max_player, game, eval_params=None):
    # Implements minimax algorithm with alpha-beta pruning
    # Returns (evaluation_score, best_move_board)
```

#### Board Evaluation Function
The evaluation function considers multiple factors:
- **Piece Count**: Difference in number of pieces
- **King Count**: Difference in number of kings
- **Move Opportunities**: Available moves for each player
- **Capture Opportunities**: Potential capture sequences
- **King Hopefuls**: Pieces that can become kings

```python
def evaluate(board, game, pieces_weight=1.0, kings_weight=1.0, 
            moves_weight=0.0, opportunities_weight=0.0, king_hopefuls_weight=0.0):
    # Evaluates board position for AI decision making
```

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- Pygame

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd checkers
   ```

2. **Install dependencies**:
   ```bash
   pip install pygame
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

### How to Play

1. **Starting the Game**: Run `main.py` to launch the graphical interface
2. **Player Controls**: 
   - Click on a piece to select it
   - Valid moves are highlighted in blue
   - Click on a highlighted square to make a move
3. **AI Turn**: The AI automatically makes its move after each player move
4. **Game End**: The game ends when one player has no pieces remaining

## 🧪 Testing

The project includes comprehensive unit tests for the AI components:

```bash
python -m unittest ai.py
```

### Test Coverage

- **Board Evaluation**: Tests for various board configurations
- **Move Generation**: Validation of legal move generation
- **AI Decision Making**: Verification of AI move selection
- **Edge Cases**: Boundary conditions and special scenarios

### Board Configurations

The `board_configs.py` file contains 25+ predefined board configurations for testing:
- Standard starting positions
- Complex mid-game scenarios
- Edge cases and special situations
- King promotion scenarios

## 📊 Game Rules Implementation

### Standard Checkers Rules
- **Movement**: Regular pieces move diagonally forward only
- **Kings**: Promoted pieces can move diagonally in any direction
- **Captures**: Pieces can capture by jumping over opponent pieces
- **Multi-hop**: Multiple captures in a single turn are mandatory
- **Promotion**: Pieces become kings when reaching the opposite edge

### Advanced Features
- **Forced Captures**: System automatically enforces capture moves
- **Move Validation**: Comprehensive validation of all move types
- **State Management**: Proper game state tracking and transitions

## 🎯 AI Strategy

### Search Algorithm
- **Depth**: Configurable search depth (default: 3)
- **Pruning**: Alpha-Beta pruning for improved performance
- **Evaluation**: Multi-factor board evaluation with configurable weights

### Evaluation Metrics
1. **Material Advantage**: Piece and king count differences
2. **Positional Advantage**: Strategic piece positioning
3. **Mobility**: Available move opportunities
4. **Tactical Advantage**: Capture opportunities and king hopefuls

## 🔧 Configuration

### Game Settings
Modify `constants.py` to adjust:
- Board size and dimensions
- Colors and visual appearance
- Game speed and timing

### AI Parameters
Adjust AI behavior in `ai.py`:
- Search depth for minimax
- Evaluation function weights
- Performance optimizations

## 📁 Project Structure

```
checkers/
├── main.py              # Game entry point and main loop
├── game.py              # Core game logic and state management
├── board.py             # Board representation and piece management
├── piece.py             # Individual piece behavior
├── ai.py                # AI implementation and evaluation
├── display.py           # Pygame-based graphical interface
├── constants.py         # Game constants and configuration
├── board_configs.py     # Predefined board configurations
├── move_node.py         # Move tree data structure
├── crown.png            # King piece visual asset
├── README.md            # This file
└── Boards.docx          # Additional documentation
```

## 🎨 Visual Interface

### Features
- **Clean Design**: Professional checkers board appearance
- **Move Highlighting**: Valid moves clearly indicated
- **Piece Selection**: Visual feedback for selected pieces
- **Smooth Animations**: Fluid game transitions
- **Responsive Controls**: Intuitive mouse-based interaction

### Customization
- Modify colors in `constants.py`
- Adjust board dimensions and spacing
- Customize piece appearance and animations

## 🔍 Technical Details

### Performance Optimizations
- **Alpha-Beta Pruning**: Reduces search space significantly
- **Efficient Move Generation**: Optimized algorithms for move calculation
- **State Management**: Minimal memory overhead
- **Pygame Optimization**: Efficient rendering and event handling

### Code Quality
- **Comprehensive Documentation**: Detailed docstrings for all functions
- **Type Hints**: Clear parameter and return type specifications
- **Error Handling**: Robust error checking and validation
- **Modular Design**: Clean separation of concerns

## 🤝 Contributing

### Development Guidelines
1. **Code Style**: Follow PEP 8 Python style guidelines
2. **Documentation**: Add docstrings for new functions
3. **Testing**: Include unit tests for new features
4. **Performance**: Consider optimization for AI components

### Potential Improvements
- **Enhanced AI**: Implement more sophisticated evaluation functions
- **Multiple AI Levels**: Add difficulty settings
- **Network Play**: Multiplayer functionality
- **Replay System**: Game recording and playback
- **Analysis Tools**: Move analysis and suggestions

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Myles Gould** - Computer Science & Mechanical Engineering Student at Northwestern University

---

*This Checkers AI implementation demonstrates advanced game theory concepts and provides a solid foundation for further development in game AI and algorithmic game theory.*

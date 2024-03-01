An educational chess game designed for single players to improve their strategic thinking. It features a powerful AI opponent who analyzes your moves, suggesting improvements based on potential captures, threats, and control over key squares.

### Key Features:

- **Single-player Mode**: Engage in a challenging match against a powerful AI opponent. 
- **Move-by-Move Analysis**: Gain valuable insights with suggested improvements for every move you make. 
- **AI Rationale Visualization**: Witness the AI's decision-making process in real-time, including:
  - Top Potential Moves: See the top 5 squares the AI considers, highlighted with varying intensity based on their evaluation. 
  - Evaluation Breakdown: Analyze each potential move with:
    - The piece being considered for movement. 
    - The target square. 
    - A visual representation of the move's evaluation (e.g., bar graph, number). 
    - Justification for the AI's evaluation (e.g., "Capture", "Threat", "Control"). 
- **Game Logging**: Track your progress by saving and loading gameplay logs for later review. 
- **Designed for Learning**: Develop your strategic thinking and chess skills through interactive analysis and guided improvement.

### Structure
```
chess_sage/
├── __init__.py        # (Optional) Empty file to mark the directory as a package
├── config.py          # Contains global configurations (e.g., board size, colors)
├── pieces.py          # Defines classes for different chess pieces
├── board.py           # Defines the chess board class, including state management and move validation
├── game.py            # Implements core game logic, including player turns, game flow, and win/lose conditions
├── ai.py              # Implements the AI algorithms (Minimax, Alpha-Beta Pruning, etc.) 
├── visualization.py    # Handles visual elements like board rendering, highlighting, and UI components
├── analysis.py        # Analyzes potential moves for the AI, including evaluations and justification logic
├── logging.py         # Handles game logging functionalities (saving/loading)
├── utils.py           # Contains utility functions used throughout the project (e.g., input validation)
└── main.py            # Entry point for the program, starts the game loop
```
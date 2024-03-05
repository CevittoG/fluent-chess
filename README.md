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
chess_sage/  # Main project directory

├── doc/                    # Subdirectory for documentation files
│   ├── ATRIBUTIONS.md          # File containing project attributions (e.g., authors, licenses)
│   ├── ROADMAP.md              # File outlining the project development roadmap
│   └── STRUCTURE.md            # File explaining the project directory structure (like this one!)
├── media/                  # Subdirectory for game assets
│   ├── fonts/                  # Subdirectory for fonts used in the game
│   │   ├── consola.ttf             
│   │   └── ...                     
│   ├── icons/                  # Subdirectory for game icons
│   │   ├── angle-double-small-right.png  
│   │   └── ...                     
│   └── images/                 # Subdirectory for game-related images
│       ├── black_bishop.png        
│       └── ...                     
└── src/                    # Subdirectory for Python code modules
    ├── __init__.py             # Optional empty file to treat the directory as a package
    ├── config.py               # Contains global configurations like board size and colors
    ├── pieces.py               # Defines classes for different chess pieces (pawn, knight, etc.)
    ├── board.py                # Defines the chess board class, managing state and move validation
    ├── game.py                 # Implements core game logic (turns, flow, win/lose conditions)
    ├── ai.py                   # Implements AI algorithms for computer opponent (Minimax, etc.)
    ├── visualization.py        # Handles visual elements like board rendering and UI
    ├── analysis.py             # Analyzes potential moves for the AI, including evaluation
    ├── logging.py              # Handles game logging functionalities (saving/loading)
    ├── utils.py                # Contains utility functions used throughout the project (e.g., input validation)
    └── main.py                 # Entry point for the program, starts the game loop

```
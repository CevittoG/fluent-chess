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
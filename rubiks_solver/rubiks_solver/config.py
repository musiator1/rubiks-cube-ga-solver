# --- SCREEN SETTINGS ---
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

# ---- COLORS SETTINGS ---
COLORS = {
    'W': (238, 238, 238),
    'Y': (255, 204, 0),
    'G': (0, 153, 34),
    'B': (34, 85, 221),
    'R': (204, 0, 0),
    'O': (238, 102, 0),
}

# --- GENETIC ALGORITHM SETTINGS ---
SHUFFLE_SEQUENCE = [
    "F", "L", "U'", "L", "U", "B",
    "U'", "R'", "B", "D", "F'", "D'",
    "F", "R", "U'", "L", "B'", "D",
    "R","U'", "L'", "B", "L'", "F'",
    "D'","F"
] + ["F'", 'D', 'R', 'L', 'B', 'U', 'U', "F'", "F'", 'U', 'U', 'U', 'F', "B'", "L'", "D'", "U'", 'R', 'D', "L'", "D'", 'D', "F'", "D'", "D'", "L'", "R'", 'D', 'U', 'L', 'U', "D'", 'U', "F'", 'B', "U'", 'D', 'U', 'F', "L'", "L'", "R'", "U'"] + ["U'", "U'", "L'", "L'", 'D', 'L', "D'", 'B', 'L', "R'", 'D', "L'", "D'", 'L', 'U', 'B', "U'", 'F', 'D', "R'", 'F', 'L', "D'", "D'", "F'", 'B', "F'", 'R', "U'", 'D', "B'"]

POPULATION_SIZE = 100
CHROMOSOME_LENGTH = (26, 50)
MAX_GENERATIONS = 1000
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2
ELITE_SIZE = 2

# --- CUBE STATES FOR STAGE APPROACH ---
STAGES_TILES = {
    "white_cross": {
        "U": [[None, "W", None], 
              ["W", "W", "W"], 
              [None, "W", None]],
              
        "D": [[None, None, None],
              [None, None, None],
              [None, None, None]],

        "F": [[None, "G", None],
              [None, None, None],
              [None, None, None]],

        "B": [[None, "B", None],
              [None, None, None],
              [None, None, None]],

        "L": [[None, "O", None],
              [None, None, None],
              [None, None, None]],
              
        "R": [[None, "R", None],
              [None, None, None],
              [None, None, None]],
    },
    "first_layer": {
        "U": [["W", "W", "W"], 
              ["W", "W", "W"], 
              ["W", "W", "W"]],
              
        "D": [[None, None, None],
              [None, None, None],
              [None, None, None]],

        "F": [["G", "G", "G"],
              [None, "G", None],
              [None, None, None]],

        "B": [["B", "B", "B"],
              [None, "B", None],
              [None, None, None]],

        "L": [["O", "O", "O"],
              [None, "O", None],
              [None, None, None]],
              
        "R": [["R", "R", "R"],
              [None, "R", None],
              [None, None, None]],
    },
    "second_layer": {
        "U": [["W", "W", "W"], 
              ["W", "W", "W"], 
              ["W", "W", "W"]],
              
        "D": [[None, None, None],
              [None, None, None],
              [None, None, None]],

        "F": [["G", "G", "G"],
              ["G", "G", "G"],
              [None, None, None]],

        "B": [["B", "B", "B"],
              ["B", "B", "B"],
              [None, None, None]],

        "L": [["O", "O", "O"],
              ["O", "O", "O"],
              [None, None, None]],
              
        "R": [["R", "R", "R"],
              ["R", "R", "R"],
              [None, None, None]],
    },
    "full_cube": {
        'U': [['W']*3 for _ in range(3)],
        'D': [['Y']*3 for _ in range(3)],
        'F': [['G']*3 for _ in range(3)],
        'B': [['B']*3 for _ in range(3)],
        'L': [['O']*3 for _ in range(3)],
        'R': [['R']*3 for _ in range(3)],
    }
}

STAGES_CUBIES = {
    "white_cross": {
        "corners": [],
        "edges": ["FU", "RU", "BU", "LU"]
    },
    "first_layer": {
        "corners": ["FLU", "FRU", "BLU", "BRU"],
        "edges": ["FU", "RU", "BU", "LU"]
    },
    "second_layer": {
        "corners": ["FLU", "FRU", "BLU", "BRU"],
        "edges": ["FU", "RU", "BU", "LU", "FR", "BL", "BR", "FL"]
    },
    "full_cube": {
        "corners": ["FLU", "FRU", "BLU", "BRU", "FLD", "FRD", "BLD", "BRD"],
        "edges": ["FU", "RU", "BU", "LU", "FR", "BL", "BR", "FL", "FD", "BD", "RD", "LD"]
    },
}
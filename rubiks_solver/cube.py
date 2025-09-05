import random

class Cube:
    """
    Representation of a 3x3 Rubik's Cube with support for moves, rotations, and shuffling::

           ___ ___ ___
         /___/___/___/│
        /___/_U_/___/││      Y
       /___/___/__ /│/│      │  Z
      │   │   │   │ /││      │ /
      │___│___│___│/R/│      │/
      │   │ F │   │ /││      o──────X
      │___│___│___│/│/
      │   │   │   │ /
      │___│___│___│/
    """

    def __init__(self):
        """Initialize solved cube state and move definitions."""
        self._init_faces()
        
        # Mapping of how face rows/cols shift during each move
        self.moves = {
            "F": [
                ('U', 2, 'row', 0),
                ('R', 0, 'col', 1),
                ('D', 0, 'row', 0),
                ('L', 2, 'col', 1),
            ],
            "B": [
                ('U', 0, 'row', 1),
                ('L', 0, 'col', 0),
                ('D', 2, 'row', 1),
                ('R', 2, 'col', 0)                
            ],
            "R": [
                ('F', 2, 'col', 0),
                ('U', 2, 'col', 1),
                ('B', 0, 'col', 1),
                ('D', 2, 'col', 0),
            ],
            "L": [
                ('F', 0, 'col', 0),
                ('D', 0, 'col', 1),
                ('B', 2, 'col', 1),
                ('U', 0, 'col', 0),
            ],
            "U": [
                ('F', 0, 'row', 0),
                ('L', 0, 'row', 0),
                ('B', 0, 'row', 0),
                ('R', 0, 'row', 0),
            ],
            "D": [
                ('F', 2, 'row', 0),
                ('R', 2, 'row', 0),
                ('B', 2, 'row', 0),
                ('L', 2, 'row', 0),                                                
            ]
        }
    
        self.all_moves_symbols = ["F", "F'", "B", "B'", "L", "L'", "R", "R'", "U", "U'", "D", "D'"]

        # Map move notation to bound methods
        self.move_funcs = {
            "F": self.F, "F'": self.F_,
            "B": self.B, "B'": self.B_,
            "L": self.L, "L'": self.L_,
            "R": self.R, "R'": self.R_,
            "U": self.U, "U'": self.U_,
            "D": self.D, "D'": self.D_,
        }

        # Opposite moves, useful for inverse operations
        self.opposite_move = {
            "F": "F'", "F'": "F",
            "B": "B'", "B'": "B",
            "L": "L'", "L'": "L",
            "R": "R'", "R'": "R",
            "U": "U'", "U'": "U",
            "D": "D'", "D'": "D",
        }

        # Corner stickers: cubelet name -> list of (face, row, col)
        self.corners = {
            "FLU": [("F", 0, 0), ("L", 0, 2), ("U", 2, 0)],
            "FRU": [("F", 0, 2), ("R", 0, 0), ("U", 2, 2)],
            "FLD": [("F", 2, 0), ("L", 2, 2), ("D", 0, 0)],
            "FRD": [("F", 2, 2), ("R", 2, 0), ("D", 0, 2)],
            "BLU": [("B", 0, 2), ("L", 0, 0), ("U", 0, 0)],
            "BRU": [("B", 0, 0), ("R", 0, 2), ("U", 0, 2)],
            "BLD": [("B", 2, 2), ("L", 2, 0), ("D", 2, 0)],
            "BRD": [("B", 2, 0), ("R", 2, 2), ("D", 2, 2)],
        }

        # Edge stickers: cubelet name -> list of (face, row, col)
        self.edges = {
            "FU": [("F", 0, 1), ("U", 2, 1)],
            "FR": [("F", 1, 2), ("R", 1, 0)],
            "FD": [("F", 2, 1), ("D", 0, 1)],
            "FL": [("F", 1, 0), ("L", 1, 2)],
            "BU": [("B", 0, 1), ("U", 0, 1)],
            "BR": [("B", 1, 0), ("R", 1, 2)],
            "BD": [("B", 2, 1), ("D", 2, 1)],
            "BL": [("B", 1, 2), ("L", 1, 0)],
            "RU": [("R", 0, 1), ("U", 1, 2)],
            "RD": [("R", 2, 1), ("D", 1, 2)],
            "LU": [("L", 0, 1), ("U", 1, 0)],
            "LD": [("L", 2, 1), ("D", 1, 0)],
        }

    def _init_faces(self):
        """Reset cube faces to solved state."""
        self.faces = {
            'U': [['W']*3 for _ in range(3)],  # White
            'D': [['Y']*3 for _ in range(3)],  # Yellow
            'F': [['G']*3 for _ in range(3)],  # Green
            'B': [['B']*3 for _ in range(3)],  # Blue
            'L': [['O']*3 for _ in range(3)],  # Orange
            'R': [['R']*3 for _ in range(3)],  # Red
        }
        
    def _rotate_face_cw(self, face_name: str, times: int = 1):
        """Rotate face clockwise by 90° * times."""
        for _ in range(times):
            self.faces[face_name] = [list(row) for row in zip(*self.faces[face_name][::-1])]
    
    def _rotate_face_ccw(self, face_name: str, times: int = 1):
        """Rotate face counter-clockwise by 90° * times."""
        for _ in range(times):
            self.faces[face_name] = [list(row) for row in zip(*self.faces[face_name])][::-1]
    
    def _cycle(self, move_name: str):
        """Cycle stickers between adjacent faces for a given move (without rotating the face itself)."""
        move = self.moves[move_name]
        
        # Extract rows/cols
        parts = []
        for face_name, idx, type, reverse in move:
            face = self.faces[face_name]
            if type == 'row':
                part = face[idx][:]
            elif type == 'col':
                part = [row[idx] for row in face]
            else:
                raise ValueError("type must be 'row' or 'col'")
            if reverse:
                part = part[::-1]
            parts.append(part)
            
        # Rotate the extracted parts
        parts = parts[-1:] + parts[:-1]
        
        # Put parts back
        for part, (face_name, idx, type, _) in zip(parts, move):
            if type == 'row':
                self.faces[face_name][idx] = part
            else:
                for r in range(3):
                    self.faces[face_name][r][idx] = part[r]
    
    def reset(self):
        """Reset cube to solved state."""
        self._init_faces()

    def shuffle(self, sequence: list[str] | None = None, lenght: int = 26) -> list[str]:
        """
        Apply a sequence of moves to the cube.

        Args:
            sequence (list[str] | None): List of moves in standard notation. If None, a random sequence is generated.
            lenght (int): Length of random shuffle sequence.

        Returns:
            list[str]: The sequence of moves that was applied.
        """
        if sequence is None:
            sequence = [random.choice(self.all_moves_symbols) for _ in range(lenght)]
        
        for move in sequence:
            self.move_funcs[move]()

        return sequence
    
    def copy(self) -> "Cube":
        """Return a deep copy of the cube state."""
        new_cube = Cube()
        new_cube.faces = {face: [row[:] for row in grid] for face, grid in self.faces.items()}
        return new_cube
    
    # ----------- Rotations of the entire cube (reorientations) -----------

    def rotate_x(self):
        """Rotate cube around X axis (R-L axis)."""
        U, F, D, B = self.faces['U'], self.faces['F'], self.faces['D'], self.faces['B']
        self.faces['U'], self.faces['F'], self.faces['D'], self.faces['B'] = F, D, B, U
        self._rotate_face_cw('B', times=2)
        self._rotate_face_cw('D', times=2)
        self._rotate_face_cw('R')
        self._rotate_face_ccw('L')

    def rotate_y(self):
        """Rotate cube around Y axis (U-D axis)."""
        F, L, B, R = self.faces['F'], self.faces['L'], self.faces['B'], self.faces['R']
        self.faces['F'], self.faces['L'], self.faces['B'], self.faces['R'] = R, F, L, B
        self._rotate_face_cw('U')
        self._rotate_face_ccw('D')

    def rotate_z(self):
        """Rotate cube around Z axis (F-B axis)."""
        U, R, D, L = self.faces['U'], self.faces['R'], self.faces['D'], self.faces['L']
        self.faces['U'], self.faces['R'], self.faces['D'], self.faces['L'] = L, U, R, D
        self._rotate_face_cw('R')
        self._rotate_face_cw('D')
        self._rotate_face_cw('L')
        self._rotate_face_cw('U')
        self._rotate_face_cw('F')
        self._rotate_face_ccw('B')
    
    # ----------- Face moves (standard Rubik's notation) -----------

    def F(self): self._cycle('F'); self._rotate_face_cw('F')
    def F_(self): [self._cycle('F') for _ in range(3)]; self._rotate_face_ccw('F')

    def B(self): self._cycle('B'); self._rotate_face_cw('B')
    def B_(self): [self._cycle('B') for _ in range(3)]; self._rotate_face_ccw('B')

    def R(self): self._cycle('R'); self._rotate_face_cw('R')
    def R_(self): [self._cycle('R') for _ in range(3)]; self._rotate_face_ccw('R')

    def L(self): self._cycle('L'); self._rotate_face_cw('L')
    def L_(self): [self._cycle('L') for _ in range(3)]; self._rotate_face_ccw('L')

    def U(self): self._cycle('U'); self._rotate_face_cw('U')
    def U_(self): [self._cycle('U') for _ in range(3)]; self._rotate_face_ccw('U')

    def D(self): self._cycle('D'); self._rotate_face_cw('D')
    def D_(self): [self._cycle('D') for _ in range(3)]; self._rotate_face_ccw('D')
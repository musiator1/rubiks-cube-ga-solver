import pytest

from rubiks_solver.cube import Cube

def test_copy_independence():
    cube = Cube()
    copy_cube = cube.copy()
    copy_cube.F()
    assert cube.faces != copy_cube.faces

def test_shuffle_should_change_state():
    shuffled = Cube()
    solved = Cube()
    shuffled.shuffle()
    assert shuffled.faces != solved.faces

def test_reset_should_restore_state():
    solved = Cube()
    reseted = Cube()
    reseted.shuffle()
    reseted.reset()
    assert solved.faces == reseted.faces

def test_opposite_moves_should_not_change_state():
    solved = Cube()
    test = Cube()
    for move, opposite_move in test.opposite_move.items():
        test.shuffle([move, opposite_move])
        assert test.faces == solved.faces
        test.reset()

def test_four_moves_sequence_repeated_six_times_should_not_change_state():
    solved = Cube()
    test = Cube()
    for _ in range(6):
        test.shuffle(["L'", "U", "L", "U'"])
    
    assert test.faces == solved.faces

def test_opposite_rotations_should_not_change_state():
    solved = Cube()
    test = Cube()
    test._rotate_face_ccw("F")
    test._rotate_face_cw("F")
    assert test.faces == solved.faces
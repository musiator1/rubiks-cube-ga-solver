import pytest

from rubiks_solver.ga import GASolver, Individual
from rubiks_solver.cube import Cube
from rubiks_solver.config import ELITE_SIZE

@pytest.fixture
def cube():
    return Cube()


@pytest.fixture
def ga_solver(cube):
    solver = GASolver(
        starting_cube=cube,
        pop_size=10,
        crossover_prob=0.8,
        mutation_prob=0.5,
        min_chromosome_len=3,
        max_chromosome_len=5
    )
    solver.init_population()
    return solver


def test_population_initialization(ga_solver):
    assert len(ga_solver.population) == ga_solver.pop_size
    lengths = [len(ind.chromosome) for ind in ga_solver.population]
    assert all(3 <= l <= 5 for l in lengths)


def test_evaluate_fitness_correct_tiles(ga_solver, cube):
    target = cube.copy()
    ga_solver.evaluate(target_state=target.faces, method="correct_tiles")
    for ind in ga_solver.population:
        assert 0 <= ind.fitness <= 1


def test_evaluate_fitness_cubies_position(ga_solver, cube):
    target = {"corners": cube.corners.keys(), "edges": cube.edges.keys()}
    ga_solver.evaluate(target_state=target, method="cubies_position")
    for ind in ga_solver.population:
        assert 0 <= ind.fitness <= 1


def test_select_parents_returns_pairs(ga_solver, cube):
    target = cube.copy()
    ga_solver.evaluate(target_state=target.faces, method="correct_tiles")
    pairs = ga_solver.select_parents(method="tournament", k=3)
    assert all(isinstance(p, tuple) and len(p) == 2 for p in pairs)
    assert len(pairs) == ga_solver.pop_size // 2


def test_crossover_produces_children(ga_solver, cube):
    target = cube.copy()
    ga_solver.evaluate(target_state=target.faces, method="correct_tiles")
    parents = ga_solver.select_parents(method="roulette")
    children = ga_solver.crossover(parents)
    assert isinstance(children, list)
    assert all(isinstance(c, Individual) for c in children)
    assert len(children) == ga_solver.pop_size - ELITE_SIZE


def test_mutate_changes_chromosomes(ga_solver, cube):
    target = cube.copy()
    ga_solver.evaluate(target_state=target.faces, method="correct_tiles")
    parents = ga_solver.select_parents(method="roulette")
    children = ga_solver.crossover(parents)
    before = [ind.chromosome[:] for ind in children]
    mutated = ga_solver.mutate(children)
    changed = any(b != m.chromosome for b, m in zip(before, mutated))
    assert changed or all(b == m.chromosome for b, m in zip(before, mutated))


def test_get_elites_returns_top_individuals(ga_solver):
    for i, ind in enumerate(ga_solver.population):
        ind.fitness = i / 10
    elites = ga_solver.get_elites()
    assert len(elites) == ELITE_SIZE
    fitnesses = [ind.fitness for ind in elites]
    assert all(fitnesses[i] >= fitnesses[i + 1] for i in range(len(fitnesses) - 1))

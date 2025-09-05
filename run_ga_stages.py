import sys

from rubiks_solver.ga import GASolver
from rubiks_solver.config import (
    POPULATION_SIZE, MAX_GENERATIONS, CROSSOVER_RATE, MUTATION_RATE,
    SHUFFLE_SEQUENCE, STAGES_TILES, STAGES_CUBIES
)
from rubiks_solver.cube import Cube


def run_stage(stage_name, cube, max_generation, min_chromosome_len, max_chromosome_len, eval_method="correct_tiles"):
    """
    Run a single GA stage for the cube.

    stage_name: key in STAGES_TILES / STAGES_CUBIES
    eval_method: "correct_tiles" or "cubies_position"
    Returns (fitness, chromosome).
    """
    stages = STAGES_TILES if eval_method == "correct_tiles" else STAGES_CUBIES
    if stage_name not in stages:
        raise ValueError(f"Unknown stage name: {stage_name}")

    ga_solver = GASolver(
        cube, POPULATION_SIZE, CROSSOVER_RATE, MUTATION_RATE,
        min_chromosome_len, max_chromosome_len
    )
    ga_solver.init_population()
    ga_solver.evaluate(target_state=stages[stage_name], method=eval_method)

    best_solution = None

    for gen in range(max_generation):
        parents = ga_solver.select_parents(method="roulette")
        children = ga_solver.crossover(parents)
        children = ga_solver.mutate(children)
        elites = ga_solver.get_elites()

        ga_solver.population = elites + children
        ga_solver.evaluate(target_state=stages[stage_name], method=eval_method)

        current_best = max(ga_solver.population, key=lambda ind: ind.fitness)
        print(f"Generation {gen}: Best fitness = {current_best.fitness:.4f}")

        if best_solution is None or current_best.fitness > best_solution.fitness:
            best_solution = current_best

        if current_best.fitness == 1.0:
            print(f"Solution found in generation {gen}")
            break
    
    return best_solution.fitness, best_solution.chromosome


def run_and_check(stage_name, cube, min_len, max_len, sequences, eval_method="cubies_position"):
    """Helper: run stage, update cube, append sequence, exit if failed."""
    print(f"\n=== {stage_name.upper()} ===")
    fitness, chromosome = run_stage(stage_name, cube, MAX_GENERATIONS, min_len, max_len, eval_method)
    sequences.append(chromosome)
    cube.shuffle(chromosome)

    if fitness == 1.0:
        print(f"{stage_name.capitalize()} finished with success!")
    else:
        print(f"{stage_name.capitalize()} finished with failure!")
        print(f"Best fitness: {fitness:.4f}, with sequences: {sequences}")
        sys.exit()


# --- Main ---
if __name__ == "__main__":
    cube = Cube()
    cube.shuffle(SHUFFLE_SEQUENCE)
    sequences = []
    eval_method = "cubies_position"

    run_and_check("white_cross", cube, 7, 10, sequences, eval_method)
    run_and_check("first_layer", cube, 20, 50, sequences, eval_method)
    run_and_check("second_layer", cube, 20, 50, sequences, eval_method)
    run_and_check("full_cube", cube, 20, 50, sequences, eval_method)

    print("Cube solved!")
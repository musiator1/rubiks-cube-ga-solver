import time
from rubiks_solver.ga import GASolver, Individual
from rubiks_solver.config import (
    POPULATION_SIZE, MAX_GENERATIONS, CROSSOVER_RATE, MUTATION_RATE,
    STAGES_CUBIES, SHUFFLE_SEQUENCE, STAGES_TILES
)
from rubiks_solver.cube import Cube

def main():
    # --- CONFIG ---
    NUM_RUNS = 1
    EVAL_METHOD = "correct_tiles" #"cubies_position"
    MIN_CHROMO_LEN = 26
    MAX_CHROMO_LEN = 50
    STAGES = STAGES_CUBIES if EVAL_METHOD == "cubies_position" else STAGES_TILES

    all_best_fitness = []
    all_times = []
    best_ever_overall = None

    for run in range(NUM_RUNS):
        print(f"\n=== Run {run + 1}/{NUM_RUNS} ===")
        start = time.perf_counter()

        cube = Cube()
        cube.shuffle(SHUFFLE_SEQUENCE)

        ga_solver = GASolver(
            starting_cube=cube,
            pop_size=POPULATION_SIZE,
            crossover_prob=CROSSOVER_RATE,
            mutation_prob=MUTATION_RATE,
            min_chromosome_len=MIN_CHROMO_LEN,
            max_chromosome_len=MAX_CHROMO_LEN,
        )
        ga_solver.init_population()
        ga_solver.evaluate(STAGES["full_cube"], method=EVAL_METHOD)

        best_ever_individual = None

        for gen in range(MAX_GENERATIONS):
            parents = ga_solver.select_parents(method="roulette")
            children = ga_solver.crossover(parents)
            children = ga_solver.mutate(children)
            elites = ga_solver.get_elites()
            ga_solver.population = elites + children
            ga_solver.evaluate(STAGES["full_cube"], method=EVAL_METHOD)

            fitness_values = [ind.fitness for ind in ga_solver.population]
            best_in_gen = max(ga_solver.population, key=lambda ind: ind.fitness)
            avg_fitness = sum(fitness_values) / len(fitness_values)

            # --- save copy of best ---
            if best_ever_individual is None or best_in_gen.fitness > best_ever_individual.fitness:
                best_ever_individual = Individual(best_in_gen.chromosome[:])
                best_ever_individual.fitness = best_in_gen.fitness

            print(f"Generation {gen}: Best fitness = {best_in_gen.fitness:.4f}, Avg fitness = {avg_fitness:.4f}")

            if best_in_gen.fitness == 1.0:
                print(f"Solution found in generation {gen}")
                break

        elapsed = time.perf_counter() - start
        all_times.append(elapsed)
        all_best_fitness.append(best_ever_individual.fitness)

        print(f"Run {run + 1} finished in {elapsed:.3f} s")
        print("Best ever chromosome this run:", best_ever_individual.chromosome)
        print("Best ever fitness this run:", best_ever_individual.fitness)

        if best_ever_overall is None or best_ever_individual.fitness > best_ever_overall.fitness:
            best_ever_overall = best_ever_individual

    # --- SUMMARY ---
    avg_best_fitness = sum(all_best_fitness) / NUM_RUNS
    avg_time = sum(all_times) / NUM_RUNS

    print("\n=== SUMMARY ===")
    print(f"Average best fitness over {NUM_RUNS} runs: {avg_best_fitness:.4f}")
    print(f"Average execution time: {avg_time:.3f} s")
    print("Best ever chromosome overall:", best_ever_overall.chromosome)
    print("Best ever fitness overall:", best_ever_overall.fitness)

if __name__ == "__main__":
    main()

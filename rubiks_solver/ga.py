import random
import heapq
import bisect

from rubiks_solver.config import ELITE_SIZE, CHROMOSOME_LENGTH

class GASolver:
    """
    Genetic Algorithm solver for Rubik's Cube.
    Manages population, evaluation, selection, crossover, and mutation.
    """

    def __init__(
        self,
        starting_cube,
        pop_size: int,
        crossover_prob: float,
        mutation_prob: float,
        min_chromosome_len: int | None = None,
        max_chromosome_len: int | None = None
    ):
        self.starting_cube = starting_cube
        self.pop_size = pop_size
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.population = []
        self.min_chromosome_len = min_chromosome_len if min_chromosome_len is not None else CHROMOSOME_LENGTH[0]
        self.max_chromosome_len = max_chromosome_len if max_chromosome_len is not None else CHROMOSOME_LENGTH[1]

    def init_population(self):
        """
        Initialize population with random chromosomes (sequences of moves).
        Avoids consecutive opposite moves.
        """
        for _ in range(self.pop_size):
            chromosome_len = random.randint(self.min_chromosome_len, self.max_chromosome_len)
            chromosome = []
            while len(chromosome) < chromosome_len:
                new_gene = random.choice(self.starting_cube.all_moves_symbols)
                if not chromosome or new_gene != self.starting_cube.opposite_move[chromosome[-1]]:
                    chromosome.append(new_gene)

            individual = Individual(chromosome)
            self.population.append(individual)

    def evaluate(self, target_state: dict, population: list | None = None, method: str = "correct_tiles"):
        """
        Evaluate fitness of population.

        Args:
            target_state (dict): Target cube state to compare against.
            population (list[Individual] | None): If None, evaluate self.population.
            method (str): "correct_tiles" or "cubies_position".
        """
        if population is None:
            population = self.population

        if method == "correct_tiles":
            self._eval_tiles(target_state, population)
        elif method == "cubies_position":
            self._eval_cubies(target_state, population)
        else:
            raise ValueError(f"Unknown evaluation method: {method}")

    def _eval_tiles(self, target_state: dict, population: list):
        """Fitness = % of correctly placed stickers compared to target_state."""
        for individual in population:
            cube = self.starting_cube.copy()
            cube.shuffle(individual.chromosome)
            correct_tiles = 0
            total = 0

            for target_face, face in zip(target_state.values(), cube.faces.values()):
                for target_row, row in zip(target_face, face):
                    for target_tile, tile in zip(target_row, row):
                        if target_tile is not None:
                            total += 1
                            if tile == target_tile:
                                correct_tiles += 1

            individual.fitness = correct_tiles / total

    def _eval_cubies(self, target_state: dict, population: list):
        """Fitness = % of correctly positioned cubies compared to target_state."""
        for individual in population:
            cube = self.starting_cube.copy()
            cube.shuffle(individual.chromosome)
            correct_cubies = 0
            total = 0
            
            # Corners
            for name, corner in cube.corners.items():
                if name in target_state["corners"]:
                    total += 1
                    if all(cube.faces[f][r][c] == cube.faces[f][1][1] for f, r, c in corner):
                        correct_cubies += 1

            # Edges
            for name, edge in cube.edges.items():
                if name in target_state["edges"]:
                    total += 1
                    if all(cube.faces[f][r][c] == cube.faces[f][1][1] for f, r, c in edge):
                        correct_cubies += 1
                        
            individual.fitness = correct_cubies / total

    def select_parents(self, method: str = "tournament", k: int = 5, c: float = 1.5):
        """
        Select parents for crossover.

        Args:
            method (str): "roulette", "tournament", or "exp_rank".
            k (int): Tournament size (for "tournament").
            c (float): Exponential base (for "exp_rank").
        """
        if method == "roulette":
            return self._roulette_selection()
        elif method == "tournament":
            return self._tournament_selection(k)
        elif method == "exp_rank":
            return self._exp_rank_selection(c)
        else:
            raise ValueError(f"Unknown selection method: {method}")

    def _roulette_selection(self):
        """Roulette-wheel selection based on fitness proportionate probability."""
        parents = []
        total_fitness = sum(ind.fitness for ind in self.population)
        cum_sum = []
        running_sum = 0
        for ind in self.population:
            running_sum += ind.fitness
            cum_sum.append(running_sum)

        for _ in range(self.pop_size):
            rand = random.random() * total_fitness
            i = bisect.bisect_left(cum_sum, rand)
            parents.append(self.population[i])

        return [(p1, p2) for p1, p2 in zip(parents[0::2], parents[1::2])]

    def _tournament_selection(self, k: int):
        """Tournament selection: pick best from random subsets of size k."""
        parents = []
        for _ in range(self.pop_size):
            tournament = random.sample(self.population, k)
            winner = max(tournament, key=lambda ind: ind.fitness)
            parents.append(winner)
        return [(p1, p2) for p1, p2 in zip(parents[0::2], parents[1::2])]

    def _exp_rank_selection(self, c: float):
        """Exponential rank-based selection with base `c`."""
        ranked = sorted(self.population, key=lambda ind: ind.fitness)
        exp_values = [c**rank for rank in range(1, len(ranked) + 1)]
        total = sum(exp_values)

        cum_sum = []
        running_sum = 0
        for val in exp_values:
            running_sum += val
            cum_sum.append(running_sum)

        parents = []
        for _ in range(self.pop_size):
            rand = random.random() * total
            i = bisect.bisect_left(cum_sum, rand)
            parents.append(ranked[i])

        return [(p1, p2) for p1, p2 in zip(parents[0::2], parents[1::2])]
    
    def crossover(self, parents: list[tuple]):
        """
        1-point crossover between parent pairs.

        Returns:
            list[Individual]: Children after crossover.
        """
        children = []

        for p1, p2 in parents:
            len1, len2 = len(p1.chromosome), len(p2.chromosome)
            min_len = min(len1, len2)

            if random.random() < self.crossover_prob and min_len > 2:
                split_idx = random.randint(1, min_len - 1)
                chromosome1 = p1.chromosome[:split_idx] + p2.chromosome[split_idx:]
                chromosome2 = p2.chromosome[:split_idx] + p1.chromosome[split_idx:]
            else:
                chromosome1 = p1.chromosome[:]
                chromosome2 = p2.chromosome[:]

            children.append(Individual(chromosome1))
            children.append(Individual(chromosome2))

        # Keep population size fixed
        children = random.sample(children, self.pop_size - ELITE_SIZE)
        return children

    def mutate(self, children: list):
        """
        Apply mutation to children with probability `mutation_prob`.

        Mutation types:
            - Modify existing gene
            - Add new gene
            - Remove a gene

        Ensures no consecutive opposite moves.
        """
        for individual in children:
            if random.random() <= self.mutation_prob:
                rand = random.random()

                # Modify gene
                if rand <= 0.33 and individual.chromosome:
                    idx = random.randrange(len(individual.chromosome))
                    gene = individual.chromosome[idx]

                    forbidden = set()
                    if idx > 0:
                        forbidden.add(self.starting_cube.opposite_move[individual.chromosome[idx - 1]])
                    if idx < len(individual.chromosome) - 1:
                        forbidden.add(self.starting_cube.opposite_move[individual.chromosome[idx + 1]])

                    available_moves = [m for m in self.starting_cube.all_moves_symbols if m not in forbidden and m != gene]
                    if available_moves:
                        individual.chromosome[idx] = random.choice(available_moves)

                # Insert new gene
                elif rand <= 0.66:
                    idx = random.randrange(len(individual.chromosome) + 1)
                    forbidden = set()
                    if idx > 0:
                        forbidden.add(self.starting_cube.opposite_move[individual.chromosome[idx - 1]])
                    if idx < len(individual.chromosome):
                        forbidden.add(self.starting_cube.opposite_move[individual.chromosome[idx]])

                    available_moves = [m for m in self.starting_cube.all_moves_symbols if m not in forbidden]
                    if available_moves:
                        individual.chromosome.insert(idx, random.choice(available_moves))

                # Remove gene
                else:
                    if len(individual.chromosome) > 1:
                        while True:
                            idx = random.randrange(len(individual.chromosome))
                            new_chromosome = individual.chromosome[:idx] + individual.chromosome[idx + 1:]
                            
                            if 0 < idx < len(new_chromosome):
                                left, right = new_chromosome[idx - 1], new_chromosome[idx]
                                if self.starting_cube.opposite_move[left] == right:
                                    continue
                            individual.chromosome = new_chromosome
                            break

        return children

    def get_elites(self):
        """Return top-ELITE_SIZE individuals from current population."""
        return heapq.nlargest(ELITE_SIZE, self.population, key=lambda ind: ind.fitness)


class Individual:
    """Representation of a GA individual (solution candidate)."""

    def __init__(self, chromosome: list[str]):
        self.chromosome = chromosome
        self.fitness: float | None = None

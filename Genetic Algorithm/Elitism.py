import random

# Represents a single solution (chromosome) to the knapsack problem
class Chromosome:
    def __init__(self, genes, items, max_weight):
        self.genes = list(genes)                  # 0 or 1 for each item (take or skip)
        self.items = items                        # List of (value, weight) pairs
        self.max_weight = max_weight
        self.fitness = self.calculate_fitness()   # Fitness score of the solution

    def calculate_fitness(self):
        total_value = 0
        total_weight = 0
        for i in range(len(self.genes)):
            if self.genes[i] == 1:  # If item is selected
                value, weight = self.items[i]
                total_value += value
                total_weight += weight

        if total_weight > self.max_weight:
            return 0  # Invalid solution if over weight
        return total_value

    def __str__(self):
        return f"Genes: {self.genes}, Fitness: {self.fitness}"


# The main Genetic Algorithm class
class GeneticAlgorithm:
    def __init__(self, max_weight, items, population_size, mutation_rate):
        self.max_weight = max_weight
        self.items = items
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self.create_initial_population()

    # Step 1: Create initial random population
    def create_initial_population(self):
        population = []
        for _ in range(self.population_size):
            genes = [random.choice([0, 1]) for _ in range(len(self.items))]
            population.append(Chromosome(genes, self.items, self.max_weight))
        return population

    # Step 2: Select parents based on fitness
    def select_parents(self):
        # Keep top 2 fittest
        sorted_pop = sorted(self.population, key=lambda c: c.fitness, reverse=True)
        best_two = sorted_pop[:2]

        total_fitness = sum(c.fitness for c in self.population)
        if total_fitness == 0:
            others = random.choices(self.population, k=self.population_size - 2)
        else:
            probabilities = [c.fitness / total_fitness for c in self.population]
            others = random.choices(self.population, weights=probabilities, k=self.population_size - 2)

        return best_two + others

    # Step 3: Crossover - mix genes of two parents
    def crossover(self, parent1, parent2):
        point = random.randint(1, len(parent1.genes) - 1)
        child1_genes = parent1.genes[:point] + parent2.genes[point:]
        child2_genes = parent2.genes[:point] + parent1.genes[point:]
        return Chromosome(child1_genes, self.items, self.max_weight), Chromosome(child2_genes, self.items, self.max_weight)

    # Step 4: Mutation - randomly flip bits
    def mutate(self, chromosome):
        for i in range(len(chromosome.genes)):
            if random.random() < self.mutation_rate:
                chromosome.genes[i] = 1 - chromosome.genes[i]
        chromosome.fitness = chromosome.calculate_fitness()

    # Step 5: Evolve population for one generation
    def evolve(self):
        new_population = []
        parents = self.select_parents()

        for i in range(0, self.population_size, 2):
            parent1 = parents[i % len(parents)]
            parent2 = parents[(i + 1) % len(parents)]
            child1, child2 = self.crossover(parent1, parent2)
            self.mutate(child1)
            self.mutate(child2)
            new_population.extend([child1, child2])

        self.population = new_population[:self.population_size]

    # Get the best solution so far
    def get_best_solution(self):
        return max(self.population, key=lambda c: c.fitness)


# Utility function to load knapsack items from a file
def load_items(file_path):
    items = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        max_weight = int(lines[0].split()[0])
        for line in lines[1:]:
            value, weight = map(int, line.split())
            items.append((value, weight))
    return max_weight, items


# Main script
if __name__ == "__main__":
    max_weight, items = load_items("test.txt")
    ga = GeneticAlgorithm(max_weight, items, population_size=10, mutation_rate=0.2)

    for _ in range(50):
        ga.evolve()

    best = ga.get_best_solution()
    print("Best solution:", best)
    print("Total fitness (value):", best.fitness)

import numpy as np
from utils import get_rules_popularity, get_sum_of_rule, get_random_rule_sign

"""
Fitness function ideas:
- the most popular rules, create weight of rules and sum them here
"""
def fitness_function(individual, popularity):
    return get_sum_of_rule(individual, popularity)

def tournament_selection(population, fitness_values, tournament_size):
    best_individual = None
    for _ in range(tournament_size):
        idx = np.random.randint(0, len(population))
        if best_individual is None or fitness_values[idx] < fitness_values[best_individual]:
            best_individual = idx
    return population[best_individual]

def crossover(parent1, parent2):
    crossover_point = np.random.randint(0, len(parent1))
    child = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    return child

"""
Replacing rules with other popular rules
"""
def mutation(individual, mutation_rate):
    # for i in range(len(individual)):
    #     if np.random.rand() < mutation_rate:
    #         individual[i] = get_random_rule_sign()
    return individual

# requires formatted rules as population
def evolutionary_algorithm(population, population_size, individual_length, num_generations, mutation_rate, tournament_size):
    popularity = get_rules_popularity(population)
    # print(popularity)
    for _ in range(num_generations):
        fitness_values = [fitness_function(individual, popularity) for individual in population]

        new_population = []
        while len(new_population) < population_size:
            parent1 = tournament_selection(population, fitness_values, tournament_size)
            parent2 = tournament_selection(population, fitness_values, tournament_size)
            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)
            new_population.append(child.tolist())
    
    # best_idx = np.argmax([fitness_function(individual) for individual in population])
    # return population[best_idx]
    return new_population
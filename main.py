from utils import format_rules, get_rules_popularity
from evol_algo import evolutionary_algorithm

if __name__ == "__main__":
    folderPath = '/Users/kamil.delekta/Erasmus/Magisterka/SetupForRulesFinder/Results/'
    filePath = '10k-most-common-google-words|7-more-passwords.txt'
    rulesPath = folderPath + filePath

    with open(rulesPath, 'r') as file:
        rules = [line.strip() for line in file.readlines()[1:-1]]   

    rules_formatted = format_rules(rules)

    # Parameters
    pop_size = 100
    individual_length = 10
    num_generations = 100
    mutation_rate = 0.01
    tournament_size = 5

    # Run the evolutionary algorithm
    # print("Before:", rules_formatted)
    best_individual = evolutionary_algorithm(rules_formatted, pop_size, individual_length, num_generations, mutation_rate, tournament_size)
    # print("After:", best_individual)

    # print('Popularity', get_rules_popularity(rules))

    """ Ideas:
    - [Infra] create automat with rulesfinder, and comparing with Hashcat so you can compare different approaches 
    """
from utils import format_rules, get_rules_popularity
from evol_algo import evolutionary_algorithm
import pandas as pd
import re
from utils_file import HASHCAT_LOGS_PATH, append_new_line, empty_file, get_effectiveness, hashcat_attack, save_evol_rules

TEST_RESULTS = '/Users/kamil.delekta/Erasmus/Magisterka/Project/effectiveness_evol_test.txt'

def save_test(pop_size, num_generations, tournament_size):
    effectiveness = get_effectiveness(HASHCAT_LOGS_PATH, 'Recovered')
    to_save = str(pop_size) + ',' + str(num_generations) + ',' + str(tournament_size) + ',' + effectiveness
    append_new_line(TEST_RESULTS, to_save)

# [WORKING]
if __name__ == "__main__":
    wordlist = '10k-most-common-google-words.txt'
    cleartext = '7-more-passwords.txt'

    # rulesfinder_result_path = extract_rules_with_rulesfinder(wordlist=wordlist, cleartext=cleartext)
    rulesfinder_result_path = './results/10k-most-common-google-words.txt_7-more-passwords.txt'
    rules_formatted = format_rules(rulesfinder_result_path)

    # Evolutionary Algorithm Parameters
    individual_length = 2
    num_generations = 20
    mutation_rate = 0.01
    tournament_size = 2
    pop_size = 100
    popularity = get_rules_popularity(rules_formatted)

    empty_file(TEST_RESULTS)
    for pop_size in range(50, 150, 50):
        for num_generations in range(20, 80, 20):
            for tournament_size in range(2, 4, 2):
                evol_rules = evolutionary_algorithm(popularity,
                                                    rules_formatted, 
                                                    pop_size, 
                                                    individual_length, 
                                                    num_generations,
                                                    mutation_rate,
                                                    tournament_size)
                save_evol_rules(evol_rules)
                hashcat_attack(wordlist=wordlist, cleartext=cleartext)
                save_test(pop_size, num_generations, tournament_size)


    result = []

    with open(TEST_RESULTS, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            parts = line.split(',')[0:3]
            match = re.search(r'\((.*?)%\)', line)
            if match:
                parts.append(match.group(1))
            to_save = ','.join(parts)
            result += [to_save]
   
    empty_file(TEST_RESULTS)
    
    with open(TEST_RESULTS, 'a') as f:
        for el in result:
            f.write(el)
            f.write('\n')

    # Read the file into a pandas DataFrame
    data = pd.read_csv(TEST_RESULTS, header=None, names=['pop_size', 'num_generations', 'tournament_size', 'effectiveness'])

    # Calculate the correlation matrix
    correlation_matrix = data.corr()

    # Print the correlation matrix
    print(correlation_matrix)
    print(correlation_matrix['effectiveness'])


   
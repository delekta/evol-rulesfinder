from utils import format_rules, get_rules_popularity
from evol_algo import evolutionary_algorithm
from datetime import datetime
import pandas as pd
import re
from utils_file import HASHCAT_LOGS_PATH, append_new_line, empty_file, get_effectiveness, hashcat_attack, save_evol_rules

EFFECTIVENESS_RESULT = '/Users/kamil.delekta/Erasmus/Magisterka/Project/effectiveness_test.txt'

def save_test(base, multiply):
    effectiveness = get_effectiveness(HASHCAT_LOGS_PATH, 'Recovered')
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    to_save = str(base) + ',' + str(multiply) + ',' + effectiveness
    append_new_line(EFFECTIVENESS_RESULT, to_save)

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

    empty_file(EFFECTIVENESS_RESULT)
    for base in range(400, 800, 100):
        for multiply in range(50, 200, 50):
            evol_rules = evolutionary_algorithm(popularity,
                                                rules_formatted, 
                                                pop_size, 
                                                individual_length, 
                                                num_generations, 
                                                mutation_rate, 
                                                tournament_size, 
                                                base,
                                                multiply)
            save_evol_rules(evol_rules)
            hashcat_attack(wordlist=wordlist, cleartext=cleartext)
            save_test(base, multiply)
            print(base, multiply)

    result = []

    with open(EFFECTIVENESS_RESULT, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            parts = line.split(',')[0:2]
            match = re.search(r'\((.*?)%\)', line)
            if match:
                parts.append(match.group(1))
            to_save = ','.join(parts)
            result += [to_save]

    empty_file(EFFECTIVENESS_RESULT)
    
    with open(EFFECTIVENESS_RESULT, 'a') as f:
        for el in result:
            f.write(el)
            f.write('\n')

    data = pd.read_csv(EFFECTIVENESS_RESULT, header=None, names=['base', 'multiply', 'effectiveness'])

    # Calculate the correlation matrix
    correlation_matrix = data.corr()

    # Print the correlation matrix
    print(correlation_matrix)
    print(correlation_matrix['effectiveness'])


   
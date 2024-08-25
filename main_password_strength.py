import random
import statistics
from zxcvbn import zxcvbn
from utils import format_rules, get_unified_rules_popularity
from evol_algo import evolutionary_algorithm
import subprocess
import matplotlib.pyplot as plt
from utils_file import EVOL_RULES_PATH, RULES_DIR, WORDLIST_DIR, append_new_line, empty_file, save_evol_rules 

PARAMETER_TEST_RESULTS = '/Users/kamil.delekta/Erasmus/Magisterka/Project/strength_result.txt'

def save_test(parameter_to_save, value, parameter_name):
    to_save = str(parameter_to_save) + ',' + str(value) + ',' + parameter_name
    append_new_line(PARAMETER_TEST_RESULTS, to_save)

def prepare_random_lines(file, num_lines, save_file):
    with open(file, 'r') as f:
        words = [line.strip() for line in f]

    num_lines = min(num_lines, len(words))
    random_words = random.sample(words, num_lines)
    with open(save_file, 'w') as f:
        for word in random_words:
            f.write(word + '\n')

def create_passwords(wordlist, rules, tag):
    random_wordlist_path = WORDLIST_DIR + 'random_wordlist.txt'
    random_rules_path = RULES_DIR + 'random_rules.txt'
    prepare_random_lines(wordlist, 10, random_wordlist_path)
    prepare_random_lines(rules, 1000, random_rules_path)
    command = f"hashcat -a 0 -m 0 {random_wordlist_path} -r {random_rules_path} --stdout > passwords_{tag}.txt"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

# Sometimes it throws an error: 'IndexError: list index out of range' when the passwords are too long
def get_avg_strength(path):
    with open(path, 'r', errors='ignore') as file:
        words = []
        for line in file:
            words += [int(zxcvbn(line.strip())['guesses_log10'])]
        # words = [int(zxcvbn(line.strip())['guesses_log10']) for line in file]
        return statistics.mean(words)

# [WORKING]
if __name__ == "__main__":
    wordlist = '10k-most-common-google-words.txt'
    cleartext = '7-more-passwords.txt'

    # rulesfinder_result_path = extract_rules_with_rulesfinder(wordlist=wordlist, cleartext=cleartext)
    rulesfinder_result_path = './results/10k-most-common-google-words.txt_7-more-passwords.txt'
    rules_formatted = format_rules(rulesfinder_result_path)

    # Have chosen the best parameters num_generations = 20, tournament_size = 2 from previous tests
    individual_length = 2
    num_generations = 20
    mutation_rate = 0.01
    tournament_size = 2
    # when it comes to generating strong passwords, we aim not merely to use popular rules, but to apply all available options
    # thats why we use get_unified_rules_popularity instead of get_rules_popularity
    popularity = get_unified_rules_popularity()
    pop_size = 10

    # create_passwords(wordlist=WORDLIST_DIR + wordlist, rules=rulesfinder_result_path, tag='rulesfinder')
    # print('rulesfinder avg strength:', get_avg_strength('./passwords_rulesfinder.txt'))
    # create_passwords(wordlist=WORDLIST_DIR + wordlist, rules=HASHCAT_DEFAULT_RULE_PATH, tag='hashcat')
    # print('hashcat avg strength:', get_avg_strength('./passwords_hashcat.txt'))

    # Clearing file before parameter test
    empty_file(PARAMETER_TEST_RESULTS)
    # [NOTE] Update the parameter name if you update parameter of the loop
    parameter_name = 'Mutation rate'
    while mutation_rate < 0.50:
        evol_rules = evolutionary_algorithm(popularity,
                                        rules_formatted, 
                                        pop_size, 
                                        individual_length, 
                                        num_generations,
                                        mutation_rate,
                                        tournament_size)
        save_evol_rules(evol_rules)
        create_passwords(wordlist=WORDLIST_DIR + wordlist, rules=EVOL_RULES_PATH, tag='evol')
        avg = get_avg_strength('./passwords_evol.txt')
        print(f'evol rulesfinder<mutation_rate:{mutation_rate}> avg strength:', avg)
        # [NOTE] Update the parameter_to_save if you update parameter of the loop
        save_test(parameter_to_save=mutation_rate, value=avg, parameter_name=parameter_name)
        mutation_rate += 0.02


    x_data = []
    y_data = []

    with open(PARAMETER_TEST_RESULTS, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            x, y = line.split(",")[0:2]  # Take first two
            x_data.append(float(x))
            y_data.append(float(y))

    plt.plot(x_data, y_data)
    plt.title(f"Num guesses_log10 vs {parameter_name}")
    plt.xlabel(parameter_name)
    plt.ylabel("Num guesses_log10")
    plt.show()

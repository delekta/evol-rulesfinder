from utils import format_rules, get_rules_popularity
from evol_algo import evolutionary_algorithm
import subprocess
import re
import matplotlib.pyplot as plt 

WORDLIST_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/wordlist/'
CLEARTEXT_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/cleartext/'
EVOL_RULES_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/evol_algo_result.txt'
HASHCAT_LOGS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_attack_logs.txt'
HASHCAT_RULESFINDER_LOGS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_rulesfinder_attack_logs.txt'
HASHCAT_RULE_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_rules/'
HASHCAT_DEFAULT_RULE_NAME = 'rockyou-30000.rule'
HASHCAT_DEFAULT_RULE_PATH = HASHCAT_RULE_DIR + HASHCAT_DEFAULT_RULE_NAME
HASHCAT_DEFAULT_RULES_LOGS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_default_attack_logs.txt'
TEST_RESULTS = '/Users/kamil.delekta/Erasmus/Magisterka/Project/effectiveness_evol_max_test.txt'


def extract_rules_with_rulesfinder(wordlist, cleartext):
    wordlist_path = WORDLIST_DIR + wordlist
    cleartext_path = CLEARTEXT_DIR + cleartext
    result_filename = wordlist + '|' + cleartext

    RESULTS_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/results/'
    result_path = RESULTS_DIR + result_filename


    ps = subprocess.Popen(("rulesfinder", "--hashcat","-w", wordlist_path,
                                "--cleartexts", cleartext_path,
                                    "-n", "50", "-t", "7", "--minsize", "3"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("tee", result_path), stdin=ps.stdout)
    ps.wait()
    return result_path

def hashcat_attack(wordlist, cleartext):
    wordlist_path = WORDLIST_DIR + wordlist
    cleartext_path = CLEARTEXT_DIR + cleartext

    ps = subprocess.Popen(("hashcat", "-m", "99999", cleartext_path, wordlist_path, '-r', EVOL_RULES_PATH, '--debug-mode=4', '--debug-file=matched.rule'), stdout=subprocess.PIPE)
    output = subprocess.check_output(("tee", HASHCAT_LOGS_PATH), stdin=ps.stdout)
    ps.wait()

def append_new_line(file_name, text_to_append):
    with open(file_name, 'a') as f:
        f.write(text_to_append)
        f.write('\n')

def extract_between(text, sub1, sub2):
    start = text.find(sub1)
    if start == -1: return None
    start += len(sub1)
    end = text.find(sub2, start)
    if end == -1: return None
    return text[start:end]

def get_line_with_phrase(file_name, phrase):
    with open(file_name, 'r') as f:
        for line in f:
            if phrase in line:
                return line

def get_effectiveness(file_name, phrase):
    line = get_line_with_phrase(file_name, phrase)
    return extract_between(line, 'Recovered........:', 'Digests')

def save_evol_rules(evol_rules):
    with open(EVOL_RULES_PATH, 'w') as f:
        for item in evol_rules:
            rule = ''.join(item)
            f.write("%s\n" % rule)

def save_test(pop_size):
    effectiveness = get_effectiveness(HASHCAT_LOGS_PATH, 'Recovered')
    to_save = str(pop_size) + ',' + effectiveness
    append_new_line(TEST_RESULTS, to_save)

def empty_file(file_name):
    with open(file_name, 'w') as file:
        pass

# [WORKING]
if __name__ == "__main__":
    wordlist = '10k-most-common-google-words.txt'
    cleartext = '7-more-passwords.txt'

    # rulesfinder_result_path = extract_rules_with_rulesfinder(wordlist=wordlist, cleartext=cleartext)
    rulesfinder_result_path = './results/10k-most-common-google-words.txt_7-more-passwords.txt'
    rules_formatted = format_rules(rulesfinder_result_path)

    # Evolutionary Algorithm Parameters
    # Have chosen the best parameters num_generations = 20, tournament_size = 2
    individual_length = 2
    num_generations = 20
    mutation_rate = 0.01
    tournament_size = 2
    pop_size = 100
    popularity = get_rules_popularity(rules_formatted)

    empty_file(TEST_RESULTS)
    for pop_size in range(50, 250, 50):
                evol_rules = evolutionary_algorithm(popularity,
                                                    rules_formatted, 
                                                    pop_size, 
                                                    individual_length, 
                                                    num_generations,
                                                    mutation_rate,
                                                    tournament_size)
                save_evol_rules(evol_rules)
                hashcat_attack(wordlist=wordlist, cleartext=cleartext)
                save_test(pop_size)
    

    result = []

    with open(TEST_RESULTS, 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            parts = line.split(',')[0:1]
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

    # Initialize empty lists for x and y data
    x_data = []
    y_data = []

    # Read the file
    with open(TEST_RESULTS, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()  # Remove trailing newline
            x, y = line.split(",")  # Split line by comma
            x_data.append(int(x))
            y_data.append(float(y))

    # Create the plot
    plt.plot(x_data, y_data)

    # Add title and labels
    plt.title("Effectiveness vs Population Size")
    plt.xlabel("population_size")
    plt.ylabel("effectiveness")

    # Show the plot
    plt.show()



   
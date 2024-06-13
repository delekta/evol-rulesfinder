from utils import format_rules, get_rules_popularity
from evol_algo import evolutionary_algorithm
import subprocess
import os


def extract_rules_with_rulesfinder():
    def is_hidden(file):
        return file.startswith('.')

    def get_files(directory):
        return [file for file in os.listdir(directory) if not is_hidden(file)]

    WORDLIST_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/wordlist/'
    CLEARTEXT_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/cleartext/'
    RESULTS_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/results/'

    wordlist_filenames = get_files(WORDLIST_DIR)
    cleartext_filenames = get_files(CLEARTEXT_DIR)
    index = 0
    result_filename = wordlist_filenames[index] + '|' + cleartext_filenames[index] + '.txt'

    wordlist_path = WORDLIST_DIR + wordlist_filenames[index]
    cleartext_path = CLEARTEXT_DIR + cleartext_filenames[index]
    result_path = RESULTS_DIR + result_filename


    ps = subprocess.Popen(("rulesfinder", "--hashcat","-w", wordlist_path,
                                "--cleartexts", cleartext_path,
                                    "-n", "50", "-t", "7", "--minsize", "3"), stdout=subprocess.PIPE)
    output = subprocess.check_output(("tee", result_path), stdin=ps.stdout)
    ps.wait()

def hashcat_attack():
    RESULTS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_attack_logs.txt'
    RULES_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/evol_algo_result.txt'
    WORDLIST_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/wordlist/rockyou.txt'
    PASSWORDS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/cleartext/7-more-passwords.txt'

    ps = subprocess.Popen(("hashcat", "-m", "99999", PASSWORDS_PATH, WORDLIST_PATH, '-r', RULES_PATH, '--debug-mode=4', '--debug-file=matched.rule'), stdout=subprocess.PIPE)
    output = subprocess.check_output(("tee", RESULTS_PATH), stdin=ps.stdout)
    ps.wait()

if __name__ == "__main__":
# 1. run rulesfinder.py with --hashcat
    extract_rules_with_rulesfinder()

# 2. you get file of rules in results directory 
# 3. then we have main.py we run our evolutionary algo, to mangle our rules
# 4. then we get evol_algo_result.txt
    folderPath = '/Users/kamil.delekta/Erasmus/Magisterka/Project/results/'
    filePath = '10k-most-common-google-words.txt|7-more-passwords.txt.txt'
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
    print("After:", best_individual)

    # TODO save best_individual to the file
    with open('./evol_algo_result.txt', 'w') as f:
        for item in best_individual:
            # concatenate all the strings in an array
            rule = ''.join(item)
            # Write each item on a new line
            f.write("%s\n" % rule)
    
# 5. then we can go with hashcat_attack.py
hashcat_attack()

# 6. then we john_attack.py
# TBD 


   
from utils import format_rules, get_rules_popularity
from evol_algo import evolutionary_algorithm
import subprocess
import os

WORDLIST_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/wordlist/'
CLEARTEXT_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/cleartext/'
EVOL_RULES_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/evol_algo_result.txt'
HASHCAT_LOGS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_attack_logs.txt'


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

if __name__ == "__main__":
    wordlist = '10k-most-common-google-words.txt'
    cleartext = '7-more-passwords.txt'
    rulesfinder_result_path = extract_rules_with_rulesfinder(wordlist=wordlist, cleartext=cleartext)

    with open(rulesfinder_result_path, 'r') as file:
        rules = [line.strip() for line in file.readlines()[1:-1]]   

    rules_formatted = format_rules(rules)

    # Evolutionary Algorithm Parameters
    pop_size = 100
    individual_length = 10
    num_generations = 100
    mutation_rate = 0.01
    tournament_size = 5

    evol_rules = evolutionary_algorithm(rules_formatted, pop_size, individual_length, num_generations, mutation_rate, tournament_size)

    with open(EVOL_RULES_PATH, 'w') as f:
        for item in evol_rules:
            rule = ''.join(item)
            f.write("%s\n" % rule)
    
    hashcat_attack(wordlist=wordlist, cleartext=cleartext)

    # TODO EXTRACT the result from the hashcat_log file and print it, save to the file
    # TODO john_attack.py


   
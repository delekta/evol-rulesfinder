from utils import format_rules, get_rules_popularity
from evol_algo import evolutionary_algorithm
import subprocess
import os
from datetime import datetime

WORDLIST_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/wordlist/'
CLEARTEXT_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/cleartext/'
EVOL_RULES_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/evol_algo_result.txt'
HASHCAT_LOGS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_attack_logs.txt'
HASHCAT_RULESFINDER_LOGS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_rulesfinder_attack_logs.txt'


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

def hashcat_attack_rulesfinder(wordlist, cleartext, rulesfinder_result_path):
    wordlist_path = WORDLIST_DIR + wordlist
    cleartext_path = CLEARTEXT_DIR + cleartext

    ps = subprocess.Popen(("hashcat", "-m", "99999", cleartext_path, wordlist_path, '-r', rulesfinder_result_path, '--debug-mode=4', '--debug-file=matched.rule'), stdout=subprocess.PIPE)
    output = subprocess.check_output(("tee", HASHCAT_RULESFINDER_LOGS_PATH), stdin=ps.stdout)
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

def save_algo_result(wordlist, cleartext):
    effectiveness = get_effectiveness(HASHCAT_LOGS_PATH, 'Recovered')
    effectiveness_rulesfinder = get_effectiveness(HASHCAT_RULESFINDER_LOGS_PATH, 'Recovered')
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    to_save = '[choose worst popularity]' + ' wordlist:' + wordlist + ', cleartext' + cleartext +  ', recovered:' + effectiveness +  ', recovered rulesfinder:' + effectiveness_rulesfinder + ', date:' + date_time
    append_new_line('/Users/kamil.delekta/Erasmus/Magisterka/Project/effectiveness.txt', to_save)

if __name__ == "__main__":
    wordlist = '10k-most-common-google-words.txt'
    cleartext = '7-more-passwords.txt'

    rulesfinder_result_path = extract_rules_with_rulesfinder(wordlist=wordlist, cleartext=cleartext)
    rules_formatted = format_rules(rulesfinder_result_path)

    # Evolutionary Algorithm Parameters
    pop_size = 100
    individual_length = 10
    num_generations = 100
    mutation_rate = 0.01
    tournament_size = 5

    evol_rules = evolutionary_algorithm(rules_formatted, pop_size, individual_length, num_generations, mutation_rate, tournament_size)

    save_evol_rules(evol_rules)
    
    hashcat_attack(wordlist=wordlist, cleartext=cleartext)
    hashcat_attack_rulesfinder(wordlist, cleartext, rulesfinder_result_path)

    save_algo_result(wordlist, cleartext)

    # TODO start thinking about the schema for 4th chapter
    # TODO john_attack.py


   
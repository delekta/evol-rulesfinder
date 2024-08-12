import random
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
HASHCAT_RULE_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_rules/'
HASHCAT_DEFAULT_RULE_NAME = 'rockyou-30000.rule'
HASHCAT_DEFAULT_RULE_PATH = HASHCAT_RULE_DIR + HASHCAT_DEFAULT_RULE_NAME
HASHCAT_DEFAULT_RULES_LOGS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_default_attack_logs.txt'
RULES_DIR = '/Users/kamil.delekta/Erasmus/Magisterka/Project/rules/'


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
    # cleartext_path = CLEARTEXT_DIR + cleartext

    ps = subprocess.Popen(("hashcat", "-m", "99999", cleartext, wordlist_path, '-r', EVOL_RULES_PATH, '--debug-mode=4', '--debug-file=matched.rule'), stdout=subprocess.PIPE)
    output = subprocess.check_output(("tee", HASHCAT_LOGS_PATH), stdin=ps.stdout)
    ps.wait()

def hashcat_attack_rulesfinder(wordlist, cleartext, rulesfinder_result_path):
    wordlist_path = WORDLIST_DIR + wordlist
    # cleartext_path = CLEARTEXT_DIR + cleartext

    ps = subprocess.Popen(("hashcat", "-m", "99999", cleartext, wordlist_path, '-r', rulesfinder_result_path, '--debug-mode=4', '--debug-file=matched.rule'), stdout=subprocess.PIPE)
    output = subprocess.check_output(("tee", HASHCAT_RULESFINDER_LOGS_PATH), stdin=ps.stdout)
    ps.wait()

def hashcat_attack_default_rules(wordlist, cleartext):
    wordlist_path = WORDLIST_DIR + wordlist
    # cleartext_path = CLEARTEXT_DIR + cleartext

    ps = subprocess.Popen(("hashcat", "-m", "99999", cleartext, wordlist_path, '-r', HASHCAT_DEFAULT_RULE_PATH, '--debug-mode=4', '--debug-file=matched.rule'), stdout=subprocess.PIPE)
    output = subprocess.check_output(("tee", HASHCAT_DEFAULT_RULES_LOGS_PATH), stdin=ps.stdout)
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
    prepare_random_lines(rules, 10000, random_rules_path)
    command = f"hashcat -a 0 -m 0 {random_wordlist_path} -r {random_rules_path} --stdout > passwords_{tag}.txt"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

def save_algo_result(wordlist, cleartext):
    effectiveness = get_effectiveness(HASHCAT_LOGS_PATH, 'Recovered')
    effectiveness_rulesfinder = get_effectiveness(HASHCAT_RULESFINDER_LOGS_PATH, 'Recovered')
    effectiveness_hashcat = get_effectiveness(HASHCAT_DEFAULT_RULES_LOGS_PATH, 'Recovered')
    now = datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    to_save = '[different cleartext than from extracting]' + ' wordlist:' + wordlist + ', cleartext' + cleartext +  ', recovered:' + effectiveness +  ', recovered rulesfinder:' + effectiveness_rulesfinder + ', recovered "'+ HASHCAT_DEFAULT_RULE_NAME +'":' + effectiveness_hashcat + ', date:' + date_time
    append_new_line('/Users/kamil.delekta/Erasmus/Magisterka/Project/effectiveness.txt', to_save)

# Passwords generator based on rulesfinder and evolutionary algorithm
if __name__ == "__main__":
    wordlist = '10k-most-common-google-words.txt'
    cleartext = '7-more-passwords.txt'

    # rulesfinder_result_path = extract_rules_with_rulesfinder(wordlist=wordlist, cleartext=cleartext)
    rulesfinder_result_path = './results/10k-most-common-google-words.txt_7-more-passwords.txt'
    rules_formatted = format_rules(rulesfinder_result_path)

    # Evolutionary Algorithm Parameters
    pop_size = 100
    min_individual_length = 2
    num_generations = 20
    mutation_rate = 0.01
    tournament_size = 2
    popularity = get_rules_popularity(rules_formatted)

    evol_rules = evolutionary_algorithm(popularity,
                                        rules_formatted, 
                                        pop_size, 
                                        min_individual_length, 
                                        num_generations,
                                        mutation_rate,
                                        tournament_size)
    save_evol_rules(evol_rules)
    create_passwords(wordlist=WORDLIST_DIR + wordlist, rules=EVOL_RULES_PATH, tag='generator')



   
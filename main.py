import random
from utils import format_rules, get_unified_rules_popularity
from evol_algo import evolutionary_algorithm
import subprocess
from utils_file import EVOL_RULES_PATH, RULES_DIR, WORDLIST_DIR, save_evol_rules

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
    prepare_random_lines(wordlist, 1, random_wordlist_path)
    prepare_random_lines(rules, 10000, random_rules_path)
    command = f"hashcat -a 0 -m 0 {random_wordlist_path} -r {random_rules_path} --stdout > passwords_{tag}.txt"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

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
    # to generate stronger passwords, higher mutation_rate is desirable
    mutation_rate = 0.20
    tournament_size = 2
    # when it comes to generating strong passwords, we aim not merely to use popular rules, but to apply all available options
    # thats why we use get_unified_rules_popularity instead of get_rules_popularity
    popularity = get_unified_rules_popularity()

    evol_rules = evolutionary_algorithm(popularity,
                                        rules_formatted, 
                                        pop_size, 
                                        min_individual_length, 
                                        num_generations,
                                        mutation_rate,
                                        tournament_size)
    save_evol_rules(evol_rules)
    create_passwords(wordlist=WORDLIST_DIR + wordlist, rules=EVOL_RULES_PATH, tag='generator')



   
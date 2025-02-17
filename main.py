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

def create_passwords(wordlist, rules, tag, max_words, max_rules):
    random_wordlist_path = WORDLIST_DIR + 'random_wordlist.txt' # prepare path to save new wordlist
    random_rules_path = RULES_DIR + 'random_rules.txt' # prepare path to save new rules
    prepare_random_lines(wordlist, max_words, random_wordlist_path)
    prepare_random_lines(rules, max_rules, random_rules_path)
    command = f"hashcat -a 0 -m 0 {random_wordlist_path} -r {random_rules_path} --stdout > passwords_{tag}.txt"

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()

# Passwords generator based on rulesfinder and evolutionary algorithm
if __name__ == "__main__":
    wordlist = 'test_wordlist.txt'
    cleartext = '7-more-passwords.txt'

    # rulesfinder_result_path = extract_rules_with_rulesfinder(wordlist=wordlist, cleartext=cleartext)
    rulesfinder_result_path = 'hashcat_rules/rockyou-30000.rule'
    # rulesfinder_result_path = './results/10k-most-common-google-words.txt_7-more-passwords.txt'
    rules_formatted = format_rules(rulesfinder_result_path)

    # Evolutionary Algorithm Parameters
    pop_size = 100
    # Note: it takes more time if you have min_individual_length > 2
    min_individual_length = 1 # it is minimal length of rules, it differs from minimal length of password
    num_generations = 1
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
    create_passwords(wordlist=WORDLIST_DIR + wordlist, rules=EVOL_RULES_PATH, tag='generator', max_words=1, max_rules=1000)
    # saves passwords to the 'passwords_generator.txt' file. Number of generated passwords is max(len(wordlist)*len(EVOL_RULES_PATH), max_words*max_rules)



   
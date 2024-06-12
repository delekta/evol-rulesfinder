import subprocess
import os

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
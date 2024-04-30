import subprocess


RULE_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/123.rule'
WORDLIST_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/wordlist2'
RESULTS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/generated_passwords'

ps = subprocess.Popen(("hashcat", "--stdout", "-r", RULE_PATH, WORDLIST_PATH), stdout=subprocess.PIPE)
output = subprocess.check_output(("tee", RESULTS_PATH), stdin=ps.stdout)
ps.wait()
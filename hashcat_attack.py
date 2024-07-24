import subprocess


RESULTS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_attack_logs.txt'
RULES_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/evol_algo_result.txt'
WORDLIST_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/wordlist/rockyou.txt'
PASSWORDS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/cleartext/8-more-passwords.txt'

ps = subprocess.Popen(("hashcat", "-m", "99999", PASSWORDS_PATH, WORDLIST_PATH, '-r', RULES_PATH, '--debug-mode=4', '--debug-file=matched.rule'), stdout=subprocess.PIPE)
output = subprocess.check_output(("tee", RESULTS_PATH), stdin=ps.stdout)
ps.wait()
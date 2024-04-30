import subprocess


RESULTS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/john_attack_logs.txt'
RESULTS_PATH2 = '/Users/kamil.delekta/Erasmus/Magisterka/Project/john_attack_logs2.txt'
RULES_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/results/10k-most-common-google-words.txt|7-more-passwords.txt.txt'
WORDLIST_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/wordlist/rockyou.txt'
PASSWORDS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/cleartext/8-more-passwords.txt'

#  --wordlist=[path to wordlist] --rule=PoloPassword [path to file]

ps = subprocess.Popen(("john",'--format=descrypt', f'--wordlist={WORDLIST_PATH}', '--rule',  RULES_PATH, PASSWORDS_PATH, '>', RESULTS_PATH2), stdout=subprocess.PIPE)
# output = subprocess.check_output(("tee", RESULTS_PATH), stdin=ps.stdout)
# ps.wait()

"""
to test john the ripper
john --format=descrypt --rules custom.rule --wordlist=password.lst hashes.txt > logs.txt

to show cracked passwords TODO this does not work for me
john --show hashes.txt
- john /Users/kamil.delekta/Erasmus/Magisterka/Project/john_test_hashes.txt --wordlist=/Users/kamil.delekta/Erasmus/Magisterka/Project/john_test_password.lst --rules /Users/kamil.delekta/Erasmus/Magisterka/Project/john_test_custom.rule 

john --wordlist=/Users/kamil.delekta/Erasmus/Magisterka/Project/john_test_password.lst --rules /Users/kamil.delekta/Erasmus/Magisterka/Project/john_test_custom.rule /Users/kamil.delekta/Erasmus/Magisterka/Project/john_test_hashes.txt
cd ~/.john
"""
import subprocess


RESULTS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/hashcat_attack_logs.txt'
RULES_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/results/10k-most-common-google-words.txt|7-more-passwords.txt.txt'
WORDLIST_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/wordlist/rockyou.txt'
PASSWORDS_PATH = '/Users/kamil.delekta/Erasmus/Magisterka/Project/cleartext/8-more-passwords.txt'

ps = subprocess.Popen(("hashcat", "-m", "99999", PASSWORDS_PATH, WORDLIST_PATH, '-r', RULES_PATH, '--debug-mode=4', '--debug-file=matched.rule'), stdout=subprocess.PIPE)
output = subprocess.check_output(("tee", RESULTS_PATH), stdin=ps.stdout)
ps.wait()

# TODO Rulesfinder hashcat difference 
# TODO Describe the difference between rulesfinder and hashcat
# TODO Should i skip the rules that are missing
# Problems:
"""
- Rulesfinder uses some rules that are not supported in -> rulesfinder is good
- My algorithm generates rules that can not be used
- Why do i get rules like this: cAz"123"
- John the ripper works only on hashed passwords
- should i hash passwords for the John the ripper openssl passwd -6 -salt xyz  yourpass "openssl passwd -6 -salt xyz  yourpass"
- cewl - custom word list generator based on url
- one rule to rule them all - files with rules that gives very good results
- john ~/hash --wordlist=words --rules /opt/OneRuleToRuleThemAll.rule https://www.youtube.com/watch?v=nNvhK1LUD48 looks like it works click some key to get an update. Enter to refresh
- Munge Dirty python script to munge dictionary words into password - leeting
- --hashcat        Only use rules that work in Hashcat for rulesfinder 
- rulesfinder -h -> interesting
- check rules only if it has required number of digits, capital letters, number of signs?
 

"""
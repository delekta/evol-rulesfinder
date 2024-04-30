import enchant
d = enchant.Dict("en_US")  
print(d.check("Jacob"))
print(d.check("child"))

# 1. Get passwords set
# 2. Try to extract methods from the password so we get base words. We create a table of rules and base words
# 3. Learn model so that you have set of the best combinations of rule

def checkRule1AndUpdateWord(word):
    if word[0].isupper():
        return chr(ord(word[0]) + 32 ) + word[1:], "rule1"

def checkRule2AndUpdateWord(word):
    if word[0].isupper():
        return chr(ord(word[0]) + 32 ) + word[1:], "rule2"

# add other rules 

# computationally expensive function
def getBaseWordAndRules(password):
    base_word = ""
    applied_rules = []
    while True:
        last_loop = True
        if checkRule1AndUpdateWord():
            last_loop = False
            password, rule1 = checkRule1AndUpdateWord(password)
            applied_rules += rule1
            if d.check(password): break
        elif checkRule2AndUpdateWord(password):
            last_loop = False
            password, rule1 = checkRule1AndUpdateWord(password)
            applied_rules += rule1
            if d.check(password): break
        # check other rules


        if last_loop:
            break


    return base_word, applied_rules


password = "Password12"
base_word, rules_sequence = getBaseWordAndRules(password)
print("Base Word:", base_word)
print("Rules Sequence:", rules_sequence)



# # Chats code
# def apply_rules(password):
#     base_word = ""
#     applied_rules = []  # List to store the sequence of applied rules
#     rule_index = 0
#     while rule_index < len(password):
#         rule_indicator = password[rule_index]
#         if rule_indicator == 'l':
#             base_word = base_word.lower()
#             applied_rules.append('l')
#         elif rule_indicator == 'u':
#             base_word = base_word.upper()
#             applied_rules.append('u')
#         elif rule_indicator == 'c':
#             base_word = base_word.capitalize()
#             applied_rules.append('c')
#         elif rule_indicator == 'C':
#             base_word = base_word[0].lower() + base_word[1:].upper()
#             applied_rules.append('C')
#         elif rule_indicator == 't':
#             base_word = base_word.swapcase()
#             applied_rules.append('t')
#         elif rule_indicator == 'r':
#             base_word = base_word[::-1]
#             applied_rules.append('r')
#         elif rule_indicator == 'd':
#             base_word += base_word
#             applied_rules.append('d')
#         elif rule_indicator == 'f':
#             base_word += base_word[::-1]
#             applied_rules.append('f')
#         elif rule_indicator == 'p':
#             repeat_index = rule_index + 1
#             repeat_count = int(password[repeat_index])
#             base_word += base_word * repeat_count
#             applied_rules.append('p' + password[repeat_index])
#             rule_index += 1  # Increment rule_index by 1 extra for 'N' in 'pN' rule
#         elif rule_indicator == 'T':
#             toggle_index = rule_index + 1
#             char_index = int(password[toggle_index]) - 1
#             char_list = list(base_word)
#             char_list[char_index] = char_list[char_index].swapcase()
#             base_word = ''.join(char_list)
#             applied_rules.append('T' + password[toggle_index])
#             rule_index += 1  # Increment rule_index by 1 extra for 'N' in 'TN' rule
#         elif rule_indicator == '$':
#             append_index = rule_index + 1
#             append_char = password[append_index]
#             base_word += append_char
#             applied_rules.append('$' + password[append_index])
#             rule_index += 1  # Increment rule_index by 1 extra for 'X' in '$X' rule
#         rule_index += 1  # Increment rule_index by 1 for next rule
#     return base_word, applied_rules

# Example usage


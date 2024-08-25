import random
import string

# sign that encodes rule and the amount of the signs it requires
RulesToSignsNumber = {
    # ':': {len: 3, args: ['char', 'num'] }, example to make get_random_rule_sign to work for all rules
    # len - length of the rule
    # args - an array that contains types of arguments for the rule
    ':': {'len': 1, 'mutation': True, 'args': [] }, # Noop - no operation # type: ignore
    'l': {'len': 1, 'mutation': True, 'args': [] }, # ToLower
    'u': {'len': 1, 'mutation': True, 'args': [] }, # ToUpper
    'c': {'len': 1, 'mutation': True, 'args': [] }, # Capitalize
    'C': {'len': 1, 'mutation': True, 'args': [] }, # InvertCapitalize 
    't': {'len': 1, 'mutation': True, 'args': [] }, # ToggleAll
    'T': {'len': 2, 'mutation': True, 'args': ['num'] }, # ToggleCase n - number
    'r': {'len': 1, 'mutation': True, 'args': [] }, # Reverse
    'd': {'len': 1, 'mutation': False, 'args': [] }, # Duplicate, does not used for mutation because creates too long passwords so zxcvbn library raise an error
    'p': {'len': 2, 'mutation': True, 'args': ['num'] }, # DupWordNTimes n - number
    'f': {'len': 1, 'mutation': True, 'args': [] }, # Reflect
    '{': {'len': 1, 'mutation': True, 'args': [] }, # RotLeft
    '}': {'len': 1, 'mutation': True, 'args': [] }, # RotRight
    '$': {'len': 2, 'mutation': True, 'args': ['char'] }, # Append(x) x - char
    '[': {'len': 1, 'mutation': True, 'args': [] }, # DeleteFirst
    ']': {'len': 1, 'mutation': True, 'args': [] }, # DeleteLast
    'D': {'len': 2, 'mutation': True, 'args': ['num'] }, # DeleteAt(n) n - number 
    'x': {'len': 3, 'mutation': True, 'args': ['num', 'num'] }, # Extract(n, m) n - number, m - number 
    'O': {'len': 3, 'mutation': True, 'args': ['num', 'num'] }, # OmitRange(n, m) n - number, m - number 
    'i': {'len': 3, 'mutation': True, 'args': ['num', 'char'] }, # InsertChar(n, c) n - number, c - char
    'o': {'len': 3, 'mutation': True, 'args': ['num', 'char'] }, # Overstrike(n, c) n - number, c - char 
    "'": {'len': 2, 'mutation': True, 'args': ['num'] }, # Truncate(n) n - number 
    's': {'len': 3, 'mutation': True, 'args': ['char', 'char'] }, # ReplaceAll(cc, c) cc - char, c - char
    '@': {'len': 2, 'mutation': True, 'args': ['char'] }, # PurgeAll(cc) cc - char
    'z': {'len': 2, 'mutation': True, 'args': ['num'] }, # DupeFirstChar(n) n - number
    'Z': {'len': 2, 'mutation': True, 'args': ['num'] }, # DupeLastChar(n) n - number
    'q': {'len': 1, 'mutation': False, 'args': [] }, # DupeAllChar, does not used for mutation because creates too long passwords so zxcvbn library raise an error
    'X': {'len': 4, 'mutation': True, 'args': ['num', 'num', 'num'] }, # ExtractInsert(n, m, o) n - number, m - number, o - number
    '4': {'len': 1, 'mutation': False, 'args': [] }, # AppendMemory
    '6': {'len': 1, 'mutation': False, 'args': [] }, # PrependMemory
    'M': {'len': 1, 'mutation': False, 'args': [] }, # Memorize
    # below are hashcat only functions
    'L': {'len': 2, 'mutation': False, 'args': ['num'] }, # BitshiftLeft n - number
    'R': {'len': 2, 'mutation': False, 'args': ['num'] }, # BitshiftRight n - number 
    'k': {'len': 1, 'mutation': False, 'args': [] }, # SwapFirstTwo
    'K': {'len': 1, 'mutation': False, 'args': [] }, # SwapLastTwo
    '*': {'len': 3, 'mutation': False, 'args': ['num', 'num'] }, # Swap(n, m) n - number, m - number
    '+': {'len': 2, 'mutation': False, 'args': ['num'] }, # Increment(n) n - number
    '-': {'len': 2, 'mutation': False, 'args': ['num'] }, # Decrement(n) n - number
    '.': {'len': 2, 'mutation': False, 'args': ['num'] }, # ReplaceWithNext(n)  n - number
    ',': {'len': 2, 'mutation': False, 'args': ['num'] }, # ReplaceWithPrior(n) n - number
    'y': {'len': 2, 'mutation': False, 'args': ['num'] }, # DupFirstString(n) n - number
    'Y': {'len': 2, 'mutation': False, 'args': ['num'] }, # DupLastString(n) n - number
    # new
    '^': {'len': 2, 'mutation': False, 'args': ['num'] }, # n - probably number as a string is safe
}
"""
parse array of string to array of arrays of single rules
"""
def format_rules(rulesfinder_result_path):
    with open(rulesfinder_result_path, 'r') as file:
        rules = [line.strip() for line in file.readlines()[1:-1]]   

    result = []
    for rule in rules:
        index = 0
        array_of_rules = []
        # print(rule)
        while index < len(rule):
            sign = rule[index:index+RulesToSignsNumber[rule[index]]['len']]
            index += RulesToSignsNumber[rule[index]]['len']
            array_of_rules += [sign]
        # print(array_of_rules)
        result += [array_of_rules]
    return result

""" Returns a dictionary of rules with its weights, then you can """
# requires formatted rules
def get_rules_popularity(rules):
    result = {}

    # prepare dictionary
    for x in RulesToSignsNumber.keys():
        result[x] = 0

    for rule in rules:
        for sign in rule:
            result[sign[0]] = result[sign[0]] + 1


    return result

# requires formatted rules
def get_unified_rules_popularity():
    result = {}

    # prepare dictionary
    for x in RulesToSignsNumber.keys():
        result[x] = 1

    return result

# requires formatted rules
def get_sum_of_rule(rule, popularity):
    index = 0
    result = 0
    for sign in rule:
        result += popularity[sign[0]]
    # print(rule, result) 
    return result

# we want to premium shorter rules. Looks like the score better
def length_value(word, base, multiply):
    return base - multiply * len(word)

def get_rule_value(rule, popularity, base, multiply):
    return get_sum_of_rule(rule, popularity) + length_value(rule, base, multiply)

def get_random_args(args_types):
    choices = {'char': string.ascii_letters, 'num': '0123456789'}
    res = ''.join(random.choice(choices[type]) for type in args_types)
    return res

def get_random_rule_sign():
    while True:
        key, value = random.choice(list(RulesToSignsNumber.items()))
        if not value['mutation']: 
            continue
        return key if value['len'] == 1 else key + get_random_args(value['args'])


import random

# sign that encodes rule and the amount of the signs it requires
RulesToSignsNumber = {
    # ':': {len: 1, args: ['char', 'num'] }, example to make get_random_rule_sign to work for all rules
    ':': 1, # Noop - no operation
    'l': 1, # ToLower
    'u': 1, # ToUpper
    'c': 1, # Capitalize
    'C': 1, # InvertCapitalize 
    't': 1, # ToggleAll
    'T': 2, # ToggleCase n - number
    'r': 1, # Reverse
    'd': 1, # Duplicate
    'p': 2, # DupWordNTimes n - number
    'f': 1, # Reflect
    '{': 1, # RotLeft
    '}': 1, # RotRight
    '$': 2, # Append(x) x - char
    '[': 1, # DeleteFirst
    ']': 1, # DeleteLast
    'D': 2, # DeleteAt(n) n - number 
    'x': 3, # Extract(n, m) n - number, m - number 
    'O': 3, # OmitRange(n, m) n - number, m - number 
    'i': 3, # InsertChar(n, c) n - number, c - char
    'o': 3, # Overstrike(n, c) n - number, c - char 
    "'": 2, # Truncate(n) n - number 
    's': 3, # ReplaceAll(cc, c) cc - char, c - char
    '@': 2, # PurgeAll(cc) cc - char
    'z': 2, # DupeFirstChar(n) n - number
    'Z': 2, # DupeLastChar(n) n - number
    'q': 1, # DupeAllChar
    'X': 4, # ExtractInsert(n, m, o) n - number, m - number, o - number
    '4': 1, # AppendMemory
    '6': 1, # PrependMemory
    'M': 1, # Memorize
    # below are hashcat only functions
    'L': 2, # BitshiftLeft n - number
    'R': 2, # BitshiftRight n - number 
    'k': 1, # SwapFirstTwo
    'K': 1, # SwapLastTwo
    '*': 3, # Swap(n, m) n - number, m - number
    '+': 2, # Increment(n) n - number
    '-': 2, # Decrement(n) n - number
    '.': 2, # ReplaceWithNext(n)  n - number
    ',': 2, # ReplaceWithPrior(n) n - number
    'y': 2, # DupFirstString(n) n - number
    'Y': 2, # DupLastString(n) n - number
    # new
    '^': 2, # n - probably number as a string is safe
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
            sign = rule[index:index+RulesToSignsNumber[rule[index]]]
            index += RulesToSignsNumber[rule[index]]
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



# TODO Enable this function so it works for all signs
def get_random_rule_sign():
    while True:
        key, value = random.sample(list(RulesToSignsNumber.items()), 1)[0]
        if value == 1:
            return key

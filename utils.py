import random

# sign that encodes  rule and the amount of the signs it requires
RulesToSignsNumber = {
    ':': 1,
    'l': 1,
    'u': 1,
    'c': 1,
    'C': 1,
    't': 1,
    'T': 2,
    'r': 1,
    'd': 1,
    'p': 2,
    'f': 1,
    '{': 1,
    '}': 1,
    '$': 2,
    '[': 1,
    # '\\[': 1, unsupported
    ']': 1,
    # '\\]': 1, unsupported
    'D': 2,
    'x': 3,
    'O': 3,
    'i': 3,
    'o': 3,
    "'": 2,
    's': 3,
    '@': 2,
    'z': 2,
    'Z': 2,
    'q': 1,
    'X': 4,
    '4': 1,
    '6': 1,
    'M': 1,
    'L': 2,
    'R': 2,
    'k': 1,
    'K': 1,
    '*': 3,
    '+': 2,
    '-': 2,
    '.': 2,
    ',': 2,
    'y': 2,
    'Y': 2,
    # new
    '^': 2,
}
"""
parse array of string to array of arrays of single rules
"""
def format_rules(rules):
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

# TODO Enable this function so it works for all signs
def get_random_rule_sign():
    while True:
        key, value = random.sample(list(RulesToSignsNumber.items()), 1)[0]
        if value == 1:
            return key

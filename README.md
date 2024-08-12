## Prerequisites

- Install [hashcat](https://github.com/hashcat/hashcat). If you are using MacOS, you can achieve this via [Homebrew](https://formulae.brew.sh/formula/hashcat).
- Install [rulesfinder](https://github.com/synacktiv/rulesfinder?tab=readme-ov-file#tldr).

## Tools

**Hashcat** is a tool used to evaluate the effectiveness of specific rules in our algorithm. It allows us to count how many passwords have been successfully cracked using our algorithm via testing.

**Rulesfinder** serves as the initial step to obtaining the first set of mangling rules. You provide a wordlist and a cleartext (a list of passwords). Rulesfinder then returns a set of rules that transform the wordlist into cleartext to crack the passwords. If you choose not to use Rulesfinder, you can still use the default rules that I have prepared. Instead of:

```python
rulesfinder_result_path = extract_rules_with_rulesfinder(wordlist=wordlist, cleartext=cleartext)
```

You can use the relative path to the default rules:

```python
rulesfinder_result_path = './results/10k-most-common-google-words.txt_7-more-passwords.txt'
```

## Context

The goal of this tool was to explore the use of evolutionary algorithms in generating dictionaries for dictionary-based cryptanalysis, using a rule-based method.

## Evaluation

I conducted four tests:

- [Effectiveness] `main_short_pass_test.py`: Rewards rules that produce short passwords to measure impact on effectiveness.
- [Effectiveness] `main_evol_parameters.py`: Tests how specific evolutionary algorithm parameters impact effectiveness.
- [Effectiveness] `main_evol_parameters_max.py`: Tests whether there is a limit to the number of rule combinations that enhance the effectiveness of the entire set.
- [Password Strength] `main_password_strength.py`: Assesses how specific parameters of the evolutionary algorithm affect the strength of the generated passwords.

## Password Generator

Additionally, `main.py` allows the tool to be used as a password generator. You can adjust any parameters associated with the evolutionary algorithm:

```python
pop_size = 100
min_individual_length = 2
num_generations = 20
mutation_rate = 0.01
tournament_size = 2
```

And run the generator:

```
python main.py
```

The resulting generated passwords will be saved in `passwords_generator.txt`.

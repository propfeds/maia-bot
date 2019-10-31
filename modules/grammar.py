from random import choice

def get_random_vowel():
    return choice(['a', 'e', 'i', 'o', 'u'])

def get_possessive(noun):
        if noun[-1]=='s':
            return noun+'\''
        else:
            return noun+'\'s'
from random import choice
from utils import vowels

def get_random_vowel():
    return choice(vowels)

def get_possessive(noun):
        if noun[-1]=='s':
            return noun+'\''
        else:
            return noun+'\'s'
from random import choice
from utils import vowels

def get_random_vowel() -> str:
    return choice(vowels)

def get_possessive(noun: str) -> str:
        if noun[-1]=='s':
            return noun+'\''
        else:
            return noun+'\'s'

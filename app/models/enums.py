from enum import Enum, auto


class Level(str, Enum):
    A1 = 'A1'
    A2 = 'A2'
    B1 = 'B1'
    B2 = 'B2'
    C1 = 'C1'
    C2 = 'C2'


class Type(str, Enum):
    tense = 'tense'
    word = 'word'
    irreg_verb = 'irregular verb'

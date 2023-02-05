from .autoname import AutoNameByCount
from enum import auto

class TauntType(AutoNameByCount):
    """
    Represents a type of taunt.
    """
    barf = auto()
    smoke = auto()
    drink = auto()
    warcry = auto()
    letsgo = auto()
from .autoname import AutoNameByCount
from enum import auto

class BotDifficulty(AutoNameByCount):
    """
    Represents the difficulty of a bot.
    """
    easy = auto()
    normal = auto()
    hard = auto()
    cruel = auto()
    random = auto()
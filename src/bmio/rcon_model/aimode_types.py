from .autoname import AutoNameByCount
from enum import auto

class AIMode(AutoNameByCount):
    """
    Represents the AI mode of the game.
    """
    default = auto()
    deactivate = auto()
    pacifist = auto()
    pathfind = auto()
    ignore_humans = auto()
    ignore_bots = auto()

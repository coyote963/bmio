from .autoname import AutoNameByCount
from enum import auto

class Mission(AutoNameByCount):
    """
    Represents a survival mission.
    """
    kill_everything = auto()
    kill_enemy = auto()
    kill_with_weapon = auto()
    deliver_weapon = auto()
    damage = auto()
    find_intel = auto()
    savior = auto()
    kill_boss = auto()
    kill_enemy_with_weapon = auto()
    defuse_bomb = auto()
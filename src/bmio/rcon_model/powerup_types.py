from .autoname import AutoNameByCount
from enum import auto

class PowerUp(AutoNameByCount):
    """
    Represents a powerup in the game.
    """
    triple_damage = auto()
    super_speed = auto()
    regeneration = auto()
    invisibility = auto()
    bfg = auto()
    random = "random"
from enum import Enum, auto

from .autoname import AutoName

    
class Team(AutoName):
    Unknown = -1
    Deathmatch = 0
    Usc = 1
    Man = 2
    Spectator = 3
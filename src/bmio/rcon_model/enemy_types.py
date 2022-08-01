from enum import Enum, auto

from .autoname import AutoName


class Enemy(AutoName):
    cannibal = auto(),
    hopper = auto(),
    blue_soldier = auto(),
    purple = auto(),
    sniper = auto(),
    flesheater = auto(),
    blue_lieutenant = auto(),
    fuschia = auto(),
    leaper = auto(),
    bomb_dude = auto(),
    demolition_guy = auto(),
    ninja = auto(),
    samurai = auto(),
    indigo = auto(),
    blue_captain = auto(),
    grandmaster = auto(),
    explodebot_5000 = auto(),
    anthropophagite = auto(),
    moxxy = auto(),
    roxxy = auto(),
    disciple = auto(),
    manling = auto(),
    operator = auto(),
    cowboy = auto(),
    archer = auto(),
    zombie = auto(),
    zhost = auto(),
    zpitter = auto(),
    zomikaze = auto(),
    doctor = auto(),

class EnemyRank(AutoName):
    normal = auto(),
    strong = auto(),
    elite = auto(),
    powerful = auto(),
    god_like = auto()
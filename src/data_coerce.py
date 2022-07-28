import json

from rcon_model import RconRequest, RconEvent, event_types, hat_types
from rcon_model import Hat, Weapon, Enemy

from loguru import logger

def get_coercions():
    return {
        ('Level', 'AttackerID', 'VictimID', 'KillerID', 'PlayerID', 'Bots', 'Alive', 'Dead', 'Amount', 'LandingX', 'LandingY', 'Cost', 'Players1', 'Players2', 'Alive1', 'Alive2', 'Score1', 'Score2') : lambda x : int(x),
        ('X', 'Y', 'FlagX', 'FlagY'): lambda x: float(x),
        ('Hat'): lambda x : Hat(int(x)),
        ('Weap1', 'Weap2', 'Equip', 'OffWeap', 'OffWeap2', 'KillerWeapon', 'NewWeapon', 'SkinWeapon',  'Weapon'):  lambda x: Weapon(int(x)),
        ('EnemyType',): lambda x : Enemy(x),
        ('IsAdmin', 'Teamkill', 'Kicked', 'Drone', 'Autobalanced', 'Headshot', 'Flawless', 'WasHome', 'Thrown', 'Host'): lambda x: bool(int(x)),
        ('EventID'): lambda x: RconEvent(int(x))
    }


def initialize_class(message: dict):
    for k, v in message.items():
        if k.endswith('Profile'):
            message[k] = event_types.PlayerProfile(**json.loads(v))
    for m_key, m_f in get_coercions().items():
        for key, val in message.items():
            if key in m_key:
                message[key] = m_f(val)
    
    class_name = message['EventID'].name
    module = __import__('rcon_model.event_types')
    try:
        class_ = getattr(module, class_name)
    except:
        logger.error('Class is not implemented yet')
        return event_types.BaseClass(**message)
    return class_(**message)



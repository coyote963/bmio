import json

from .rcon_model import RconRequest, RconEvent, event_types, hat_types
from .rcon_model import Hat, Weapon, Enemy

from loguru import logger

from .rcon_model.request_cases import RequestCase

def get_coercions():
    return {
        ('Level', 'AttackerID', 'VictimID', 'KillerID', 'PlayerID', 'Bots', 'Alive', 
            'Dead', 'Amount', 'LandingX', 'LandingY', 'Cost', 'Players1',
            'Players2', 'Alive1', 'Alive2', 'Score1', 'Score2') : lambda x : int(x),
        ('X', 'Y', 'FlagX', 'FlagY'): lambda x: float(x),
        
        ('Hat'): lambda x : Hat(int(x)),
        
        ('Weap1', 'Weap2', 'Equip', 'OffWeap', 'OffWeap2', 'KillerWeapon', 'NewWeapon',
            'SkinWeapon',  'Weapon'):  lambda x: Weapon(int(x)),
        
        ('EnemyType',): lambda x : Enemy(x),
        
        ('IsAdmin', 'Teamkill', 'Kicked', 'Drone', 'Autobalanced', 'Headshot', 'Flawless',
            'WasHome', 'Thrown', 'Host'): lambda x: bool(int(x)),
        ('EventID'): lambda x: RconEvent(int(x))
    }


def convert_request_data(request_data: dict):
    request_case = RequestCase(int(request_data['CaseID']))
    if request_case == RequestCase.request_match:
        return event_types.request_data_match(**request_data)
    elif request_case == RequestCase.request_player:
        return event_types.request_data_player(**request_data)
    else:
        return event_types.BaseClass(**request_data)


def is_request_data(message: dict):
    return 'CaseID' in message and 'RequestID' in message


def initialize_class(message: dict):
    """
        Main function: coerces the types of the incoming message to be the types that the classes expect.
    """
    for k, v in message.items():
        if k.endswith('Profile') and 'ProfileID' in v and 'StoreID' in v:
            message[k] = event_types.PlayerProfile(**json.loads(v))
    
    # Convert the various strings to their types
    for m_key, m_f in get_coercions().items():
        for key, val in message.items():
            if key in m_key:
                message[key] = m_f(val)
    
    # Return the request data type instead of normal type
    if is_request_data(message):
        return convert_request_data(message)

    class_name = message['EventID'].name
    module = __import__('bmio')
    try:
        class_ = getattr(module.rcon_model, class_name)
    except:
        logger.error('Class is not implemented yet')
        return event_types.BaseClass(**message)
    return class_(**message)



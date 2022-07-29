import random

from time import sleep
from rcon_model import RconEvent, RconRequest, Command
from rcon_model.event_types import log_message, player_death, player_get_powerup, request_data_match, request_data_player
from bmio import Bmio

# Create a Bmio
app = Bmio('localhost', 42070, 'admin')


# Register a handler
@app.handler(RconEvent.log_message)
def do_something(some_data: log_message):
    '''Print into the console whenever something is written to the logs'''
    print(some_data.Message)



# Request some data, when it returns callback is called
@app.handler(RconEvent.log_message)
def get_info(some_data: log_message):
    '''Print some information about the server'''
    def callback(x: request_data_match):
        print(f'Server Name: {x.ServerName} - Running on: {x.Version}')

    if 'stoptime' in some_data.Message:
        app.request_data(
            RconRequest.request_match,
            callback
        )


# Send a command: Send a message when they die.
@app.handler(RconEvent.player_death)
def player_spawn(death_info: player_death):
    '''Send a random message!'''
    app.send_command(Command.say, random.choice([
        'Try harder!',
        'You have died',
        'Be careful next time',
        'Get back up and keep trying',
        'Try again',
        'Uh Oh',
        'Whoa',
        'Wow'
    ]))



# Send a command when the data is available
@app.handler(RconEvent.player_get_powerup)
def someone_got_powerup(powerup_info: player_get_powerup):
    '''Explodes anyone that gets a powerup'''
    def callback(player: request_data_player):
        app.send_command(Command.explodebig, powerup_info.X, powerup_info.Y)
    
    app.request_data(
        RconRequest.request_player,
        callback,
        powerup_info.PlayerID
    )


# Run it!
app.run()
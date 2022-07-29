import random

from time import sleep
from rcon_model import RconEvent, RconRequest, Command
from rcon_model.event_types import chat_message, command_entered, log_message, player_death, player_get_powerup, request_data_match, request_data_player
from bmio import Bmio

# Create a Bmio
app = Bmio()


maps = [
    "maps\\stock\\arctic",
    "maps\\stock\\arena",
    "maps\\stock\\city",
    "maps\\stock\\desert",
    "maps\\stock\\factory",
    "maps\\stock\\desertcity",
    "maps\\stock\\fields",
    "maps\\stock\\fields_two",
    "maps\\stock\\lake",
    "maps\\stock\\mines",
    "maps\\stock\\railroad",
    "maps\\stock\\rooftops",
    "maps\\stock\\sewers",
    "maps\\stock\\snow",
    "maps\\stock\\tutorial",
    "maps\\stock\\throne",
    "maps\\stock\\warehouse",
    "maps\\stock\\water",
]


# Register a handler
@app.handler(RconEvent.log_message)
def do_something(some_data: log_message):
    '''Print into the console whenever something is written to the logs'''
    print(some_data.Message)



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
        'Wow',
        'Dont give up!',
    ]))

@app.handler(RconEvent.chat_message)
def remote_admin(chat: chat_message):
    if chat.Message.startswith('!'):
        app.send_request(chat.Message[1:], RconRequest.command)


@app.handler(RconEvent.chat_message)
def change_map(chat: chat_message):
    if chat.Message.startswith('>'):
        if chat.Message[1:].isnumeric():
            map_index = int(chat.Message[1:])
            app.send_command(Command.changemap, maps[map_index])


@app.handler(RconEvent.command_entered)
def command_response(command: command_entered):
    if command.ReturnText:
        app.send_command(Command.say, f'{command.ReturnText} [{command.Command}]')


# Run it!
app.run()
from enum import Enum

class RconRequest(Enum):
	login = 0
	ping = 1
	command = 2
	request_player = 3
	request_bounce = 4
	request_match = 5
	confirm = 6
	request_scoreboard = 7


from rcon_model import RconEvent
from rcon_model.event_types import log_message
from rcon_observer import RconObserver

app = RconObserver('localhost', 42070, 'admin')

@app.handledr(RconEvent.log_message)
def do_something(some_data: log_message):
    print(some_data.Message)

app.run()
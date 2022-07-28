from rcon_model import RconEvent
from rcon_model.event_types import log_message
from bmio import Bmio

# Create a Bmio
app = Bmio('localhost', 42070, 'admin')

# Register a handler
@app.handler(RconEvent.log_message)
def do_something(some_data: log_message):
    print(some_data.Message)

# Run it!
app.run()
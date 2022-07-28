# BMIO

Boring Man Rcon Scripting made simple

First initialize the boring man rcon connection.
`app = Bmio('localhost', 42070, 'admin')`

Then register some events with the provided annotation:
```
@app.handledr(RconEvent.log_message)
def do_something(some_data: log_message):
    print(some_data.Message)
```


And finally, call run() and BMIO handles the rest
`app.run()`

Voila! You now have an RCON bot that prints out the log messages

Let BMIO handle the type conversions and connection logic, so you have more time to create fun scripts!

## What's Next
Completion of type coercions: Flag data, Team information still needs to be completed
Gamestate stores for gamemode specific Bmios

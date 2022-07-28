# BMIO

Boring Man Rcon Scripting made simple

```python
# Create a Bmio
app = Bmio('localhost', 42070, 'admin')

# Register a handler
@app.handler(RconEvent.log_message)
def do_something(some_data: log_message):
    print(some_data.Message)

# Run it!
app.run()
```


Voila! You now have an RCON bot that prints out the log messages

Let BMIO handle the type conversions and connection logic, so you have more time to create fun scripts!

## What's Next
Completion of type coercions: Flag data, Team information still needs to be completed
Gamestate stores for gamemode specific Bmios

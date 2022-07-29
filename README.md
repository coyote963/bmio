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

Features
 - Enums for just about every ID type, so you don't have write magic number checks in your code
 - Automatically retry if one of the handlers fails
 - Configure the level of concurrency for the size of the server
 - Callback functions for handling data requests
 - Sending commands has never been easier! 


## What's Next
 - Completion of type coercions: Flag data, Team information still needs to be completed
 - Gamestate stores for gamemode specific Bmios
 - Finish implementation of scoreboard object
 - pypi publish

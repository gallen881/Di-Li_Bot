import json
import os

line_assess_token = input('Enter your Line Bot channel assess token:\n')
line_channel_secret = input('Enter your Line Bot channel secret:\n')
port = int(input('Enter your Line Bot webhook port:\n'))
discord_token = input('Enter your Discord Bot token:\n')
discord_prefix = input('Enter your Discord Bot prefix:\n')
discord_guild_id = int(input('Enter your Discord guild id:\n'))

config = {
    "LineBot": {
        "ACCESS_TOKEN": line_assess_token,
        "CHANNEL_SECRET": line_channel_secret,
        "host": "0.0.0.0",
        "port": port
    },
    "DiscordBot": {
        "token": discord_token,
        "prefix": discord_prefix,
        "guild_id": discord_guild_id
    }
}

with open('config.json', 'w') as file:
    json.dump(config, file, indent=4)

data = {
    "user_table": {},
    "group_table": {},
    "webhook_table": {},
    "logs_channel": {}
}

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)

os.mkdir('temp')
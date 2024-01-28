import json

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
    "last_timestamp": {
        "message": 0,
        "file": 0,
        "image": 0,
        "video": 0,
        "audio": 0,
        "sticker": 0,
        "join": 0
    },
    "user_table": {},
    "group_table": {}
}

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)

switcher = {
    "message": {
        "timestamp": 0
    },
    "join": {
        "timestamp": 0
    },
    "file": {
        "timestamp": 0
    },
    "image": {
        "timestamp": 0
    },
    "sticker": {
        "timestamp": 0
    },
    "video": {
        "timestamp": 0
    },
    "audio": {
        "timestamp": 0
    }
}

with open('switcher.json', 'w') as file:
    json.dump(switcher, file, indent=4)
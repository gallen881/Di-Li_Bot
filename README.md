# Di-Li Bot
Use Discord to send and receive messages from Line

## Supported messages type

| Message type | Line to Discord | Discord to Line |
|-|-|-|
| Text | ⭕ | ⭕ |
| Emoji | ⭕ | ⭕ |
| Stickers | ⭕ | ❌ |
| Pictures | ⭕ | ⭕ |
| Videos | ⭕ | ⭕ |
| Audios | ⭕ | ⭕ |
| Files | ⭕ | ❌ |

## How to use
1. Create a Line bot(messaging API), and get the channel access token and channel secret.
2. Create a Discord bot, and get the discord bot token.
3. Create a Discord guild, and get the guild ID.
4. Run `setup.py`, and enter the necessary informations.
5. Run `pip install -r requirements.txt`.
6. Run `Dbot.py` and `Lbot.py`.
7. Type `{your_prefix}setup` in the guild's channel.
    > example: !setup, -setup or +setup ...
8. Send some messages to the Line bot and enjoy.

## Feel Free to PR
from cogs import send
from config.settings import *


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=NOW_PLAYING))
    print(f"We have logged in as {client.user}")


# COMMAND_HANDLERS = {
#     'traduci': send.translations,
#     'cerca': send.texts_found,
#     'random': send.random_quote
# }
#
#
# async def handle_command(command, args, msg, bot_client):
#     if command not in COMMAND_HANDLERS:
#         return
#     cmd_obj = COMMAND_HANDLERS[command]
#
#
# async def handle_message(msg):
#     text = msg.content
#     if text.startswith(COMMAND_PREFIX) and text != COMMAND_PREFIX:
#         cmd_split = text[len(COMMAND_PREFIX):].split()
#         await handle_command(cmd_split[0].lower(), cmd_split[1:], msg, client)


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.startswith('?lat help'):
        pass

    elif msg.content.startswith('?lat traduci '):
        await send.translations(msg)

    elif msg.content.startswith('?lat cerca '):
        await send.texts_found(msg)

    elif '?lat random' in msg.content:
        await send.random_quote(msg)


client.run(TOKEN)

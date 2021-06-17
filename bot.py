from cogs import send
from config.settings import *
# https://discord.com/api/oauth2/authorize?client_id=843959367115341876&permissions=2148001856&scope=bot


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=NOW_PLAYING))
    print(f"We have logged in as {client.user}")


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

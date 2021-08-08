from cogs.latin import search
from cogs.embed import *
from random import choice
from config.settings import client
import json


async def texts_found(msg):
    f, v = search(msg.content.replace('?lat cerca ', ''))
    await msg.channel.send(embed=embed_texts(f, v))
    await wait_for_reply(msg, f, v)


def check(m, msg, f, v):
    if m.content.startswith('?lat cerca '):
        return True
    if not all((m.author == msg.author, m.channel == msg.channel, m.content.isdigit())):
        return False
    return 0 < int(m.content) <= len(f[:5]) + len(v[:5])


async def wait_for_reply(msg, f, v):
    try:
        m = (await client.wait_for('message', check=lambda s: check(s, msg, f, v), timeout=60.0)).content
    except asyncio.TimeoutError:
        return
    if m.startswith('?lat cerca '):  # stops if same user starts another of this event
        return
    i = int(m) - 1  # index
    link = f[i][0] if i <= len(f[:5])-1 else v[i - len(f[:5])][0]
    await msg.channel.send(embed=embed_reply(link))


async def translations(msg):
    tr = msg.content.lower().replace('?lat traduci ', '').split()
    for chunk in (tr[i:i + 20] for i in range(0, len(tr), 20)):
        await msg.channel.send(embed=embed_translations(chunk))


async def random_quote(msg):
    with open('cogs/quotes.json') as fp:
        data = json.load(fp)
        lat, ita = choice(list(data.items()))
    await msg.channel.send(f"**{lat}**\n{ita}")

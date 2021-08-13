from commands.base_command import BaseCommand
from utils.latin import search, text_info
from discord import Embed
import asyncio


class Search(BaseCommand):

    def __init__(self):
        description = "Searches for latin texts"
        params = ['text']
        super().__init__(description, params)

    async def handle(self, params, message, client):
        f, v = search(" ".join(params))
        await message.channel.send(embed=embed_texts(f, v))
        await wait_for_reply(message, f, v, client)


def embed_texts(f: list[tuple[str, str]], v: list[tuple[str, str, str]]) -> Embed:
    d = f"{len(f)} fras{'e' if len(f)==1 else 'i'} e {len(v)} version{'e' if len(v)==1 else 'i'} di cui mostro i primi"
    embed = Embed(title="Testi trovati", description=d, color=0x4B8BBE)
    # Sometimes my genius is frightening
    f = [f"{_} [{i[1]}]({i[0]})" for i, _ in zip(f, range(1, 6))]  # "f" stands for "frasi"
    v = [f"{_} [{i[1]}]({i[0]})\n*{i[2]}*" for i, _ in zip(v, range(len(f)+1, len(f)+6))]  # "v" stands for "versioni"
    embed.add_field(name="Frasi", value="\n".join(f) if f else "Nessuna frase trovata", inline=False)
    embed.add_field(name="Versioni", value="\n".join(v) if v else "Nessauna versione trovata", inline=False)
    embed.set_footer(text=f"Inviare un numero fino a {len(f[:5])+len(v[:5])}.")
    return embed


def embed_reply(link: str) -> Embed:
    title, text = text_info(link)
    embed = Embed(color=0x4B8BBE)
    embed.set_author(name="Splash Latino", icon_url="https://www.latin.it/logo/150x150/latino.png")
    text += f"\n\n**[CLICCARE QUI PER LA TRADUZIONE SU SPLASH LATINO]({link})**\n"
    embed.add_field(name=title, value=text, inline=False)
    embed.set_footer(text="Can't display translation due to Copyright © Splash! All rights reserved.")
    return embed


def check(m, msg, f, v):
    if m.content.startswith('?lat cerca '):
        return True
    if not all((m.author == msg.author, m.channel == msg.channel, m.content.isdigit())):
        return False
    return 0 < int(m.content) <= len(f[:5]) + len(v[:5])


async def wait_for_reply(msg, f, v, client):
    try:
        m = (await client.wait_for('message', check=lambda s: check(s, msg, f, v), timeout=60.0)).content
    except asyncio.TimeoutError:
        return
    if m.startswith('?lat cerca '):  # stops if same user starts another of this event
        return
    i = int(m) - 1  # index
    link = f[i][0] if i <= len(f[:5])-1 else v[i - len(f[:5])][0]
    await msg.channel.send(embed=embed_reply(link))

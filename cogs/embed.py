from .latin import latin, text_info, mouseover
from discord import Embed  # errors.HTTPException
import asyncio


async def embed_translations_desktop(tr: list[str], send):
    # embed = Embed(description="*Traduzione v. desktop*", color=0x4B8BBE)
    embed = Embed(description="*Traduzione v. desktop*", color=0x4B8BBE)
    for word in tr:
        for i, j, k in await asyncio.create_task(latin(word)):
            print(word)
            paradigm = i if j else "\u200b"  # It's super rare that the value length is higher than the limit of 1024
            translation = ", ".join(j[:5]) if j else "*Nessun risultato*"  # Same here: value limit error is super rare
            info = f'[(i)]({k} "{mouseover(word).replace("(","").replace(")","")}")'
            hover = info if len(info) <= 1024 else "\u200b"
            if len(embed.fields) == 24 or len(embed)+len(translation+paradigm+hover+word)+6 > 6000:
                print(len(embed.fields))
                await send(embed=embed)
                embed.clear_fields()
            embed.add_field(name=f"**{word}**", value=translation, inline=True)
            embed.add_field(name="\u200b", value=paradigm, inline=True)
            embed.add_field(name="\u200b", value=hover, inline=True)
    # print(len(embed))
    print(len(embed.fields))
    await send(embed=embed)


async def embed_translations_mobile(tr: list[str], send):
    embed = Embed(description="*Traduzione v. mobile*", color=0x4B8BBE)
    for word in tr:
        value = "\n".join([f"({i[0]}) {', '.join(i[1][:5])}" for i in await asyncio.create_task(latin(word))])
        if len(embed.fields) == 25 or len(embed)+len(value+word)+4 > 6000:
            await send(embed=embed)
            embed.clear_fields()
        embed.add_field(name=f"**{word}**", value=value if value else "*Nessun risutato*", inline=False)
    await send(embed=embed)


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
    embed.set_author(name="Splash Latino", icon_url="http://www.latin.it/logo/150x150/latino.png")
    text += f"\n\n**[CLICCARE QUI PER LA TRADUZIONE SU SPLASH LATINO]({link})**\n"
    embed.add_field(name=title, value=text, inline=False)
    embed.set_footer(text="Can't display translation due to Copyright © Splash! All rights reserved.")
    return embed

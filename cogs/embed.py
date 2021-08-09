from .latin import latin, text_info
from discord import Embed  # errors.HTTPException


def embed_translations(tr: list[str]) -> Embed:
    embed = Embed(title="Traduzione", color=0xFF5733)
    for word in tr:
        values = [f"({i[0]}) {', '.join(i[1][:5])}" for i in latin(word)]
        embed.add_field(name=f"**{word}**", value="\n".join(values) if values else "*Nessun risutato*", inline=False)
    return embed


def embed_texts(f: list[tuple[str, str]], v: list[tuple[str, str, str]]) -> Embed:
    d = f"{len(f)} fras{'e' if len(f)==1 else 'i'} e {len(v)} version{'e' if len(v)==1 else 'i'} di cui mostro i primi"
    embed = Embed(title="Testi trovati", description=d)
    # Sometimes my genius is frightening
    f = [f"{_} [{i[1]}]({i[0]})" for i, _ in zip(f, range(1, 6))]  # "f" stands for "frasi"
    v = [f"{_} [{i[1]}]({i[0]})\n*{i[2]}*" for i, _ in zip(v, range(len(f)+1, len(f)+6))]  # "v" stands for "versioni"
    embed.add_field(name="Frasi", value="\n".join(f) if f else "Nessuna frase trovata", inline=False)
    embed.add_field(name="Versioni", value="\n".join(v) if v else "Nessauna versione trovata", inline=False)
    embed.set_footer(text=f"Inviare un numero fino a {len(f[:5])+len(v[:5])}.")
    return embed


def embed_reply(link: str) -> Embed:
    title, text = text_info(link)
    embed = Embed()
    embed.set_author(name="Splash Latino", icon_url="http://www.latin.it/logo/150x150/latino.png")
    text += f"\n\n**[CLICCARE QUI PER LA TRADUZIONE SU SPLASH LATINO]({link})**\n"
    embed.add_field(name=title, value=text, inline=False)
    embed.set_footer(text="Can't display translation due to Copyright © Splash! All rights reserved.")
    return embed

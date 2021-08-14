import asyncio
from commands.base_command  import BaseCommand
from latin.latin            import latin, mouseover
from discord                import Embed


class Translate(BaseCommand):

    def __init__(self):
        description = "Translates latin text to italian"
        params = ['text']
        super().__init__(description, params)

    async def handle(self, params, message, client):
        async with message.channel.typing():
            send = send_mobile if message.author.is_on_mobile() else send_desktop
            await send(params, message.channel.send)


async def send_desktop(tr: list[str], send):

    embed = Embed(description="*Translation (desktop)*", color=0x4B8BBE)

    for word in tr:

        for i, j, k in await asyncio.create_task(latin(word)):

            paradigm = i if j else "\u200b"  # It's super rare that the value length is higher than the limit of 1024
            translation = ", ".join(j[:5]) if j else "*Not found*"  # Same here: value limit error is super rare
            info = f'[(i)]({k} "{mouseover(word).replace("(", "").replace(")", "")}")'
            hover = info if len(info) <= 1024 else "\u200b"

            if len(embed.fields) == 24 or len(embed) + len(translation + paradigm + hover + word) + 6 > 6000:
                await send(embed=embed)
                embed.clear_fields()

            embed.add_field(name=f"**{word}**", value=translation, inline=True)
            embed.add_field(name="\u200b", value=paradigm, inline=True)
            embed.add_field(name="\u200b", value=hover, inline=True)

    await send(embed=embed) if embed.fields else await send("Nothing found")


async def send_mobile(tr: list[str], send):

    embed = Embed(description="*Translation (mobile)*", color=0x4B8BBE)

    for word in tr:

        value = "\n".join([f"({i[0]}) {', '.join(i[1][:5])}" for i in await asyncio.create_task(latin(word))])

        if len(embed.fields) == 25 or len(embed)+len(value+word)+4 > 6000:
            await send(embed=embed)
            embed.clear_fields()

        embed.add_field(name=f"**{word}**", value=value if value else "*Nessun risutato*", inline=False)

    await send(embed=embed)

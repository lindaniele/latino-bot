import json
from commands.base_command  import BaseCommand
from random                 import choice


class Random(BaseCommand):

    def __init__(self):
        description = "Random latin quote w/ translation"
        params = []
        super().__init__(description, params)

    async def handle(self, params, message, client):
        with open('utils/quotes.json') as fp:
            data = json.load(fp)
            lat, ita = choice(list(data.items()))
        await message.channel.send(f"**{lat}**\n{ita}")

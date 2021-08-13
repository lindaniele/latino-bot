import sys
from config import settings
import discord
import message_handler

this = sys.modules[__name__]
this.running = False


def main():
    print("Starting up...")

    intents = discord.Intents.all()
    intents.presences = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        if this.running:
            return

        this.running = True

        if settings.NOW_PLAYING:
            print("Setting NP game", flush=True)
            await client.change_presence(
                activity=discord.Game(name=settings.NOW_PLAYING))
        print("Logged in!", flush=True)

    async def common_handle_message(message):
        text = message.content
        if text.startswith(settings.COMMAND_PREFIX) and text != settings.COMMAND_PREFIX:
            cmd_split = text[len(settings.COMMAND_PREFIX):].split()
            try:
                await message_handler.handle_command(cmd_split[0].lower(), cmd_split[1:], message, client)
            except Exception:
                print("Error while handling message", flush=True)
                raise

    @client.event
    async def on_message(message):
        await common_handle_message(message)

    @client.event
    async def on_message_edit(before, after):
        await common_handle_message(after)

    client.run(settings.BOT_TOKEN)


if __name__ == "__main__":
    main()

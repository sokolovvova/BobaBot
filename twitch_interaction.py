import LOGGER
import db_interaction
import osu_interaction
import settings
import msg_analyze

from twitchio.ext import commands

import util

db_interaction.init()


class Bot(commands.Bot):
    LOGGER.log("Bot started")

    def get_current_channel(self, channel):  # in: channel, out: channel index in list
        return self.connected_channels.index(channel) if channel in self.connected_channels else None

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...

        super().__init__(token=settings.TWITCH_ACCESS_TOKEN, prefix='?',
                         initial_channels=[item[1] for item in settings.USER_DATA])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        LOGGER.log(f'Logged in as | {self.nick}')
        LOGGER.log(f'User id is | {self.user_id}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        ch = self.get_current_channel(message.channel)

        if ch is not None:
            result = await msg_analyze.analyze_msg(message.content, message.channel.name, message.author.name)
            if result != "error":
                await bot.connected_channels[ch].send(result)

        await self.handle_commands(message)
        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Here we have a command hello, we can invoke our command with our prefix and command name
        # e.g ?hello
        # We can also give our commands aliases (different names) to invoke with.

        # Send a hello back!
        # Sending a reply back to the channel is easy... Below is an example.
        await ctx.send(f'Hello {ctx.author.name}!')


    """@commands.command()
    async def iq(self, ctx: commands.Context):
        msg = "https://a0.anyrgb.com/pngimg/994/898/pepe-the-frog-pol-autism-4chan-tree-frog-internet-meme-frog-meme-amphibian-playstation-4.png"
        await ctx.send(msg)"""

    @commands.command()
    async def rs(self, ctx: commands.Context):
        user_data = util.user_data_list_from_channel_name(ctx.channel.name)
        if user_data[4] == 1:
            msg = osu_interaction.get_last_played_map(ctx.channel.name)
            await ctx.send(msg)


bot = Bot()
bot.run()

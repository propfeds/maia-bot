import cogs
import discord
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot
        # self._debug_state: bool=False

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        for guild in self.bot.guilds:
            cogs.get_guild_cfg(guild)

        print(f'{self.bot.user.name}, rolling out in the age of {discord.__version__}!')

        if cogs._global.get('playing'):
            game: str=cogs._global['playing']
            await self.bot.change_presence(activity=discord.Game(game))
            print(f'Playing: {game}')
    
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
            cogs.get_cmd(guild)

        print(f'{self.bot.user.name}, rolling out in the age of {discord.__version__}!')

        if cogs._cmd['play'].get('game'):
            game: str=cogs._cmd['play']['game']
            await self.bot.change_presence(activity=discord.Game(game))
            print(f'Playing: {game}')
    
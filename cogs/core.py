import cogs
from .calc import Calculator
from .dice import Dice
from .enquiries import Enquiries
from .fluff import Fluff
from .wiki import Wiki
import discord
from discord.ext import commands
import os
from typing import Dict, Type

class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot
        self._cog_aliases: Dict[str, Type[commands.Cog]]={
            'calc': Calculator, 'calculator': Calculator,
            'dice': Dice, 
            'enquiries': Enquiries, 'inquiries': Enquiries,
            'fluff': Fluff, 'meme': Fluff, 'joke': Fluff,
            'wiki': Wiki,
        }
        self._running_cogs: set=set()

    async def report_cogs(self) -> None:
        cog_list: list=[]
        for cog in self._running_cogs:
            cog_list.append(cog.__name__)
        await self.bot.change_presence(activity=discord.Game(
            ', '.join(cog_list)))

    async def construct_cog(self, name: str, online: bool) -> str:
        name_lower=name.lower()
        if not self._cog_aliases.get(name_lower):
            # This one prints to console because it's related to autoruns
            print(f'Load failed: cog name \'{name}\' cannot be found.')
            return cogs._resp['play']['404']
        else:
            cog_type: Type[commands.Cog]=self._cog_aliases[name_lower]
            if cog_type in self._running_cogs:
                # This one too
                print(f'Cog \'{cog_type}\' is already running.')
                return cogs._resp['play']['already_running'].format(
                    cog_type.__name__)
            else:
                self._running_cogs.add(cog_type)
                self.bot.add_cog(cog_type(self.bot))
                if online:
                    await self.report_cogs()
                return None

    async def destruct_cog(self, name: str) -> str:
        name_lower=name.lower()
        if not self._cog_aliases.get(name_lower):
            # No need to print
            # print(f'Termination failed: cog name \'{name}\' cannot be found.')
            return cogs._resp['stop']['404']
        else:
            cog_type: Type[commands.Cog]=self._cog_aliases[name_lower]
            if cog_type not in self._running_cogs:
                # print(f'Cog \'{cog_type}\' is not running.')
                return cogs._resp['stop']['not_running'].format(
                    cog_type.__name__)
            else:
                self._running_cogs.remove(cog_type)
                self.bot.remove_cog(cog_type.__name__)
                await self.report_cogs()
                return None

    def load_guild_cfg(self, guild: discord.Guild) -> None:
        if not os.path.exists('data/guilds/'):
            os.mkdir('data/guilds/')

        # Guild config contains role IDs for Lorekeeps, Botkeeps and Mutes. If not
        # found, creates a blank slate so every command would fail intentionally.
        cogs._guild[guild.id]=cogs.load_cfg(f'guilds/{guild.id}', {
            'botkeep': 0,
            'lorekeep': 0,
            'mute': 0
        })

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        for guild in self.bot.guilds:
            self.load_guild_cfg(guild)

        print(f'{self.bot.user.name}, rolling out in the age of {discord.__version__}!')

        await self.report_cogs()

    @commands.command(**cogs._cmd['play'])
    async def play(self, ctx: commands.Context, *title: str) -> None:
        title_full: str=' '.join(title)
        if title_full in ('Debug', 'debug'):
            await self.bot.change_presence(status=discord.Status.dnd)
            return
        response=await self.construct_cog(title_full, True)
        if response:
            await ctx.send(response)
    
    @commands.command(**cogs._cmd['stop'])
    async def stop(self, ctx: commands.Context, *title: str) -> None:
        title_full: str=' '.join(title)
        if title_full in ('Debug', 'debug'):
            await self.bot.change_presence(status=discord.Status.online)
            return
        response=await self.destruct_cog(title_full)
        if response:
            await ctx.send(response)

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
            'calc': Calculator, 'calculator': Calculator, 'Calc': Calculator,
            'Calculator': Calculator,
            'dice': Dice, 'Dice': Dice, 
            'enquiries': Enquiries, 'inquiries': Enquiries,
            'Enquiries': Enquiries, 'Inquiries': Enquiries,
            'fluff': Fluff, 'meme': Fluff, 'joke': Fluff, 'Fluff': Fluff,
            'wiki': Wiki, 'Wiki': Wiki,
        }
        self._running_cogs: set=set()

    def construct_cog(self, name: str) -> str:
        if not self._cog_aliases.get(name):
            # This one prints to console because it's related to autoruns
            print(f'Load failed: cog name \'{name}\' cannot be found.')
            return cogs._resp['play']['404']
        else:
            cog_type: Type[commands.Cog]=self._cog_aliases[name]
            if cog_type in self._running_cogs:
                # This one too
                print(f'Cog \'{cog_type}\' is already running.')
                return cogs._resp['play']['already_running'].format(
                    cog_type.__name__)
            else:
                self._running_cogs.add(cog_type)
                self.bot.add_cog(cog_type(self.bot))

                return None

    def destroy_cog(self, name: str) -> str:
        if not self._cog_aliases.get(name):
            # No need to print
            # print(f'Termination failed: cog name \'{name}\' cannot be found.')
            return cogs._resp['stop']['404']
        else:
            cog_type: Type[commands.Cog]=self._cog_aliases[name]
            if cog_type not in self._running_cogs:
                # print(f'Cog \'{cog_type}\' is not running.')
                return cogs._resp['stop']['not_running'].format(
                    cog_type.__name__)
            else:
                self._running_cogs.remove(cog_type)
                self.bot.remove_cog(cog_type.__name__)

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

        if cogs._global.get('status'):
            game: str=cogs._global['status']
            await self.bot.change_presence(activity=discord.Game(game))
            print(f'Playing: {game}')

    @commands.command(**cogs._cmd['play'])
    async def play(self, ctx: commands.Context, *title: str) -> None:
        title_full: str=' '.join(title)
        if title_full in ('Debug', 'debug'):
            await self.bot.change_presence(status=discord.Status.dnd)
            return
        response=self.construct_cog(title_full)
        if response:
            await ctx.send(response)
    
    @commands.command(**cogs._cmd['stop'])
    async def stop(self, ctx: commands.Context, *title: str) -> None:
        title_full: str=' '.join(title)
        if title_full in ('Debug', 'debug'):
            await self.bot.change_presence(status=discord.Status.online)
            return
        response=self.destroy_cog(title_full)
        if response:
            await ctx.send(response)
    
    # @commands.command(**cogs._cmd['play'])
    # async def play(self, ctx: commands.Context, *game: str) -> None:
    #     role_botkeep: discord.Role=cogs.get_role(ctx.guild,
    #         cogs._guild[ctx.guild.id]['botkeep'])
    #     if role_botkeep not in ctx.author.roles:
    #         await ctx.send(cogs._resp['play']['403'])
    #         return
    # 
    #     game_full: str=' '.join(game)
    # 
    #     if game_full=='':
    #         await ctx.send(cogs._resp['play']['404'])
    #         return
    #     elif game_full in ('Debug', 'debug'):
    #         await self.bot.change_presence(activity=discord.Game('Debug'),
    #             status=discord.Status.dnd)
    #         cogs._global['status']='Debug'
    #         with open('data/config.json', 'w+', encoding='utf-8'
    #         ) as json_global:
    #             dump(cogs._global, json_global, sort_keys=True, indent=4)
    #     elif game_full in ('Nothing, nothing'):
    #         await self.bot.change_presence(activity=None,
    #             status=discord.Status.online)
    #         # Export status for use next launch
    #         prev_game=cogs._global.pop('status')
    #         await ctx.send(cogs._resp['play']['nothing'].format(prev_game))
    #         with open('data/config.json', 'w+', encoding='utf-8'
    #         ) as json_global:
    #             dump(cogs._global, json_global, sort_keys=True, indent=4)
    #     else:
    #         if cogs._resp['play'].get(game_full):
    #             await ctx.send(cogs._resp['play'][game_full])
    #         await self.bot.change_presence(activity=discord.Game(game_full),
    #             status=discord.Status.online)
    #         # Export status for use next launch
    #         cogs._global['status']=game_full
    #         with open('data/config.json', 'w+', encoding='utf-8'
    #         ) as json_global:
    #             dump(cogs._global, json_global, sort_keys=True, indent=4)


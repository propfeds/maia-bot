import cogs
import discord
from discord.ext import commands
from json import dump

class Core(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot=bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        for guild in self.bot.guilds:
            cogs.load_guild_cfg(guild)

        print(f'{self.bot.user.name}, rolling out in the age of {discord.__version__}!')

        if cogs._global.get('playing'):
            game: str=cogs._global['playing']
            await self.bot.change_presence(activity=discord.Game(game))
            if game=='Debug':
                await self.bot.change_presence(status=discord.Status.dnd)
            print(f'Playing: {game}')
    
    @commands.command(**cogs._cmd['play'])
    async def play(self, ctx: commands.Context, *game: str) -> None:
        role_botkeep: discord.Role=cogs.get_role(ctx.guild,
            cogs._guild[ctx.guild.id]['botkeep'])
        if role_botkeep not in ctx.author.roles:
            await ctx.send(cogs._resp['play']['403'])
            return

        game_full: str=' '.join(game)

        if game_full=='':
            await ctx.send(cogs._resp['play']['404'])
            return
        elif game_full in ('Debug', 'debug'):
            await self.bot.change_presence(activity=discord.Game('Debug'),
                status=discord.Status.dnd)
            cogs._global['playing']='Debug'
            with open('data/global.json', 'w+', encoding='utf-8'
            ) as json_global:
                dump(cogs._global, json_global, sort_keys=True, indent=4)
        elif game_full in ('Nothing, nothing'):
            await self.bot.change_presence(activity=None,
                status=discord.Status.online)
            # Export status for use next launch
            prev_game=cogs._global.pop('playing')
            await ctx.send(cogs._resp['play']['nothing'].format(prev_game))
            with open('data/global.json', 'w+', encoding='utf-8'
            ) as json_global:
                dump(cogs._global, json_global, sort_keys=True, indent=4)
        else:
            if cogs._resp['play'].get(game_full):
                await ctx.send(cogs._resp['play'][game_full])
            await self.bot.change_presence(activity=discord.Game(game_full),
                status=discord.Status.online)
            # Export status for use next launch
            cogs._global['playing']=game_full
            with open('data/global.json', 'w+', encoding='utf-8'
            ) as json_global:
                dump(cogs._global, json_global, sort_keys=True, indent=4)


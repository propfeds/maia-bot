import os
import discord
from dotenv import load_dotenv

load_dotenv()
token=os.getenv('DISCORD_TOKEN')
guild_propane=int(os.getenv('DISCORD_GUILD_PROPANE'))
prefix_help=os.getenv('COMMAND_PREFIX_HELP')

client=discord.Client()

@client.event
async def on_ready():
    guild=client.get_guild(guild_propane)
    print(f'{client.user}, enter:\n'
        f'{guild.name}(id: {guild.id})')

@client.event
async def on_message(message):
    if message.author==client.user:
        return
    
    if message.content==prefix_help+'maia':
        await message.channel.send('Beep boop!')

client.run(token)
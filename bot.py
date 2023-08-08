import discord
from discord.ext import commands
import os
import asyncio


intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print(f"{client.user} has connected to discord!")


client.remove_command('help')


@client.command()
async def help(ctx):
    embed = discord.Embed(title="Hi, I am Alisaie, What I can do for you?", description="Here is what I can do for you", color=0xDC143C)
    embed.add_field(name="!file", value="return the token file", inline=False)
    embed.add_field(name="!hello", value="response how are you", inline=False)
    embed.add_field(name="!greet", value="greeting everyone", inline=False)
    embed.add_field(name="!play + number 1-10",value="play song names 1 - 10 from your directory", inline=False)
    embed.add_field(name="!stop", value="stop playing music", inline=False)
    embed.set_image(url="https://media.tenor.com/ytnXSzt7zmMAAAAC/alisaie-shadowbringers.gif")
    await ctx.send(embed=embed)


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    # bad words filter
    badWord = ['badword']
    if any(word in message.content for word in badWord):
        await message.delete()
        await message.channel.send('Do not say bad words!')

    # Message Handling
    elif message.content == '!ping':
        await message.channel.send('pong')

    elif message.content == '!hello':
        await message.channel.send('How are you!')

    elif message.content == '👍':
        await message.add_reaction('😄')

    elif message.content == '!greet':
        await message.channel.send('Hello everyone @everyone!')

    elif message.content == '!file':
        try:
            with open('music_bot.txt', 'rb') as f:
                await message.channel.send(file=discord.File(f))
        except FileNotFoundError:
            print('File not found!')

    # Play Music and stop
    elif message.content.startswith('!play'):
        # Check if the message author is in a voice channel
        if message.author.voice is None:
            await message.channel.send('You must be in a voice channel to use this command!')
            return

        # Check if the bot is already in a voice channel
        if message.guild.voice_client is not None:
            await message.channel.send('I am already playing audio in a voice channel!')
            return

        # Parse the song number from the message content
        try:
            song_number = int(message.content.split(' ')[1])
        except IndexError:
            await message.channel.send('Please specify a song number!')
            return
        except ValueError:
            await message.channel.send('Invalid song number!')
            return

        # Get the path to the MP3 file
        file_path = os.path.join(os.getcwd(), f'{song_number}.mp3')

        # Check if the file exists
        if not os.path.isfile(file_path):
            await message.channel.send('File not found!')
            return

        # Connect to the voice channel
        voice_channel = message.author.voice.channel
        vc = await voice_channel.connect()

        # Play the MP3 file
        source = discord.FFmpegPCMAudio(
            executable='D:/ffmpeg/bin/ffmpeg.exe', source=file_path)
        vc.play(source)

        # Wait until the audio is finished playing
        while vc.is_playing():
            await asyncio.sleep(0.1)

        # Disconnect from the voice channel
        await vc.disconnect()

    elif message.content == '!stop':
        # Get the voice client
        vc = message.guild.voice_client

        # Stop the audio if it is playing or paused
        if vc:
            vc.stop()
            await vc.disconnect()

    else:
        await client.process_commands(message)

client.run(" ")

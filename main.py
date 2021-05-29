


try:
    import conf
except ImportError:
    pass



import fight

import discord.ext
import json
import os
import random
from discord.ext import commands
import discord
import img_handler as imhl
import youtube_dl
from discord.utils import get
from discord import FFmpegPCMAudio
from os import system

import fight as f






# Define "bot"
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", case_insensitive=True, intents=intents)
bot.remove_command('help')
players = {}
song_played=[]





@bot.event
async def on_ready():
    print("бот готов")


whitelist = {
    #guild_id => {hcannel_id => "guild_name / channel name"}
    822806350886207538: {825309543427866625: "Bots / nikita-bot"}
}

# Декоратор - чекер @allowed_channel  -> True/ False
def allowed_channel():
    async def predicate(ctx:commands.Context):
        #если guild id и channel id валидны => True
        if ctx.guild.id in whitelist:
            if ctx.channel.id in whitelist[ctx.guild.id].keys():
                return True

        # await ctx.channel.send("you'ra on wrong floor buddly")
        return False
    return commands.check(predicate)



        

    


# errors
@bot.event 
@allowed_channel()
async def on_command_error(ctx, error):
    
    
        embed = discord.Embed(
        title='',
        color=discord.Color.red())
        if isinstance(error, commands.CommandNotFound):
            pass
        if isinstance(error, commands.MissingPermissions):
            embed.add_field(name=f'Invalid Permissions', value=f'You dont have {error.missing_perms} permissions.')
            await ctx.send(embed=embed)
        else:
            embed.add_field(name = f':tools: ОШИБКА', value = f"```{error}```")
            await ctx.send(embed = embed)
            raise error

    


# help
@bot.command(name='help', aliases=['commands', '', 'command'])
@allowed_channel()
async def help(ctx):
    
        msg = f"**`!repeat (текст)`** - повторить текст\n" \
            f"**`!about @id`** - информация о человеке\n" \
            f"**`!ping`** - ваш пинг\n" \
            f"**`!get_channels`** - каналы сервера\n" \
            f"**`!get_members`** - участники сервера\n" 
        emb = discord.Embed(title=f"команды бота:\n", description=msg, colour=discord.Color.blurple())
        await ctx.send(embed=emb)




@bot.command(name = 'flip')
@allowed_channel()
async def flip(ctx):
    
        responses = [
                    "ОРЁЛ",
                    "РЕШКА"
                    ]
        await ctx.send(f'{random.choice(responses)}')



# повторюха
@bot.command()
@allowed_channel()
async def repeat(ctx):
    
        if ctx.message.content == "!repeat":
            await ctx.send(f'Мне нечего повторять :/')
        else:
            await ctx.send(f'{ctx.message.content[7:]}')



# информация о пользователе
@bot.command()
@allowed_channel()
async def about(ctx, member: discord.Member = None, guild: discord.Guild = None):
    
        if member == None:
                if ctx.message.author.activity == None:
                    status = "Нету"
                else:
                    status = ctx.message.author.activity
                emb = discord.Embed(title="Информация о пользователе", color=discord.Color.dark_gold())
                emb.add_field(name="Отображаемое имя:", value=ctx.message.author.display_name, inline=False)
                emb.add_field(name="Имя аккаунта:", value=ctx.message.author, inline=False)
                emb.add_field(name="id пользователя:", value=ctx.message.author.id, inline=False)

                emb.set_thumbnail(url=ctx.message.author.avatar_url)
                await ctx.send(embed=emb)
        else:
            if member.bot == True:
                await ctx.send("nope")
            else:
                if member.activity == None:
                    status = "nope"
                else:
                    status = member.activity
                emb = discord.Embed(title="Информация о пользователе", color=member.color)
                emb.add_field(name="Отображаемое имя:", emb = discord.Embed(title=f"Your ping\n", description=f'{round(bot.latency * 1000)}ms', colour=discord.Color.dark_green()), inline=False)
                emb.add_field(name="Имя аккаунта:", value=member, inline=False)
                emb.add_field(name="id пользователя:", value=member.id, inline=False)
                emb.set_thumbnail(url=member.avatar_url)
                await ctx.send(embed=emb)



# hello
@bot.command()
@allowed_channel()
async def hello(ctx):
    
        await ctx.send(f"Привет, {ctx.author.name}")



# список каналов сервера
@bot.command()
@allowed_channel()
async def get_channels(ctx):
    
        n = 1
        msgg = ""
        for i in ctx.guild.channels:
            msgg += f"**`{n}`**: **{i}**  -  *{i.id}*\n"
            n += 1
        emb = discord.Embed(title=f"Каналы этого сервера:\n", description=msgg, colour=discord.Color.dark_green())
        await ctx.send(embed=emb)


# список участников сервера
@bot.command()
@allowed_channel()
async def get_members(ctx):
    
        n = 1
        msgg = ""
        for i in ctx.guild.members:
            msgg += f"**`{n}`**: **{i}**  -  *{i.id}*\n"
            n += 1
        emb = discord.Embed(title=f"Участники этого сервера:\n", description=msgg, colour=discord.Color.dark_green())
        await ctx.send(embed=emb)




# пинг
@bot.command()
@allowed_channel()
async def ping(ctx):
    
        emb = discord.Embed(title=f"Your ping\n", description=f'{round(bot.latency * 1000)}ms', colour=discord.Color.dark_green())
        await ctx.send(embed=emb)




    


@bot.command()
@allowed_channel()
async def mka(ctx, f1: discord.Member = None,  f2: discord.Member = None ):
    
    
        if f1 and f2:
            
            responses = [
                    
                    f1.nick,
                    f2.nick
                    ]
            await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url, f1.nick, f2.nick)

            await ctx.channel.send( file= discord.File(os.path.join("./img/result.gif")))
            await ctx.send(f'{random.choice(responses)} одержал победу')




@bot.command(name="join")
@allowed_channel()
async def vc_join(ctx):
    
    

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client == None:
                    msg = f"Подключаюсь к {voice_channel.name}"
                    await ctx.channel.send(msg)
                    await voice_channel.connect()
        else:
                    msg = f"Бот уже подключен к каналу"
                    await ctx.channel.send(msg)

@bot.command(name="leave")
@allowed_channel()
async def vc_leave(ctx):
    
    

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client != None:
            msg = f"Отключаюсь от {voice_channel.name}"
            await ctx.channel.send(msg)
            await ctx.voice_client.disconnect()
        else:
            msg = f"Бот уже отключен от канала"
            await ctx.channel.send(msg)



@bot.command(name="ost")
@allowed_channel()
async def vc_ost(ctx):
    
        voice_client = discord.utils.get(bot.voice_clients, guild = ctx.guild)
        msg = f"baaaatttllleee"
        await ctx.channel.send(msg)
        await voice_client.play( discord.FFmpegPCMAudio(executable= "./sound/ffmpeg.exe", source= "./sound/mk.mp3"))
        await voice_client(discord.FFmpegPCMAudio(source="./sound/mk.mp3"))






@bot.command(name="fight")
@allowed_channel()
async def fight(ctx:commands.Context):
    # Первый претендент
    f1:discord.Member = None
    # Второй претендент
    f2:discord.Member = bot.user
    # Voice-канал участника
    voice_channel = ctx.author.voice.channel
    if voice_channel:
        await vc_join(ctx)
        # Список активных пользователей
        voice_members = voice_channel.members
        # Фильтруем пользователей, оставляя только людей
        voice_members = [member for member in voice_members if member.bot == False]
        # Отбираем претендентов
        if len(voice_members) > 1:
            # a,b = [1, 2]   => a = 1    b = 2
            f1, f2 = [voice_members.pop(random.randint(0, len(voice_members)-1)), voice_members.pop(random.randint(0, len(voice_members)-1))]
        else:
            f1 = ctx.author
        # СОЗДАТЬ VS_SCREEN
        await imhl.vs_create_animated(f1.avatar_url, f2.avatar_url)

        embed = discord.Embed(
            title = "Let's Mortal Kombat Begins!",
            description = f'{f1.display_name} бьётся с {f2.display_name}',
            colour = discord.Colour.dark_purple(),
        )

        message = await ctx.channel.send(embed = embed, file=discord.File(os.path.join("./img/result.gif")))
        # ЗАПУСТИТЬ МУЗЫКУ
        voice_client = discord.utils.get(bot.voice_clients, guild = ctx.guild)
        await voice_client.play(discord.FFmpegPCMAudio(source="./mp3/mk.mp3"))

        await f.create_fighters(f1, f2, message)


        await voice_client.stop()

        
    else: 
        await ctx.channel.send("Зайдите в voice-канал пожажя")












@bot.command()
@allowed_channel()
async def pause(ctx):
    
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            await ctx.send("аудио на паузе")
        else:
            await ctx.send("Currently no audio is playing.")


@bot.command()
@allowed_channel()
async def resume(ctx):
    
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            await ctx.send("продолжим кайф")
        else:
            await ctx.send("мы уже кайфуем")


@bot.command()
@allowed_channel()
async def stop(ctx):
    
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        voice.stop()
        await ctx.send("ну стоп так стоп")





@bot.command(pass_context=True, brief="play a song !play [url]")
@allowed_channel()
async def play(ctx, url: str):
    
        
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except Exception:
            await ctx.send("подожи пока доиграет")
            return
        await ctx.send("играет: " + url)
        voice = get(bot.voice_clients, guild=ctx.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        voice.volume = 100
        voice.is_playing()



bot.run(os.environ["BOT_TOKEN"])

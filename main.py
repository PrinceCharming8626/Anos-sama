import os
from keep_alive import keep_alive
# from pistonapi import PistonAPI
from googlesearch import search 
from discord.ext import commands
import wikipedia
import discord
import io
import re
import contextlib
import datetime
import asyncio
import random

bot = commands.Bot(
	command_prefix="+",  # Change to desired prefix
	case_insensitive=True  # Commands aren't case-sensitive
)

bot.author_id = 894969735207329893  # Change to your discord id!!!

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.do_not_disturb,activity=discord.Game("+ help "))
    print(f'{bot.user} succesfully logged in!')

@bot.command()
async def hi(ctx):
    await ctx.send(f'Hello {ctx.message.author.display_name}' )  #or ctx.message.author
  
@bot.command()
async def serverlist(ctx):
    if ctx.author.id == 894969735207329893:  #this means this commend is only for mentioned ids only.
        msg = "\n".join(f"{x}" for x in bot.guilds)
        tembed = discord.Embed(title="All Bots Guilds",description=f"```\n{msg}\n```",color=0xffff4d)
        await ctx.send(embed=tembed)

@bot.command()
async def wiki(ctx, *, arg=None):
    try:
        if arg == None:
            await ctx.send("Please, specify what do you want me to search")
        elif arg:
            start = arg.replace(" ", "")
            end = wikipedia.summary(start)
            await ctx.send(end)
    except:
        try:
            start = arg.replace(" ", "")
            end = wikipedia.summary(start, sentences=10)
            await ctx.send(end)
        except:
            await ctx.send("I can't send info because I got an unknown reference")

@bot.command()
async def coin(ctx):
    r = random.randrange(1, 101)
    if r > 5:
        d = random.randrange(1, 3)
        if d == 1:
            await ctx.send(':full_moon:')
        else:
            await ctx.send(':new_moon:')
    else:
        await ctx.send(':last_quarter_moon:')

# # Create a new Piston API instance
# piston = PistonAPI()
# print(piston.runtimes)
    
# # Execute your own code!
# @bot.command(name="eval")
# async def eval(ctx, *, code):
#   async with ctx.channel.typing():
#      codes = str(code)
#      output = piston.execute(language="py", version="3", code=codes)
#      #embed = discord.Embed(title="\n**__Your Eval Output is__** ", description=f"```{output}```", color=0xffff4d)
#      #embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
#      author=ctx.author.mention
#      #await ctx.send(embed=embed)
#      await ctx.send(f"Here is your py(3.10.0) output {author}\n```{output}```")


@bot.command(aliases=["eval", "e"])
async def evaluate(ctx, *, command):
    async with ctx.channel.typing():
        author=ctx.author.mention
        if match := re.fullmatch(r"(?:\n*)?`(?:``(?:py(?:thon)?\n)?((?:.|\n)*)``|(.*))`", command, re.DOTALL):
            code = match.group(1) if match.group(1) else match.group(2)
            str_obj = io.StringIO()  # Retrieves a stream of data
            try:
                with contextlib.redirect_stdout(str_obj):
                    exec(code)
            except Exception as e:
                return await ctx.send(f"""{author} I only received py(3.10.0) error output
```
{e.__class__.__name__}: {e}
```""")
            return await ctx.send(f"""Here is your py(3.10.0) output {author}
```
{str_obj.getvalue()}
```""")

        embed = discord.Embed(description="Error: Invalid format", color=ctx.author.color)
        return await ctx.send(embed=embed)


@bot.command()
async def rev(ctx, *, var):
    stuff = var[::-1]
    embed = discord.Embed(description=f"Your output is\n```{stuff}```", color=0xffff4d)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.message.delete()
    await ctx.send(embed=embed)

@bot.command()
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 300:
            await ctx.send("I can't count up to 5 minutes")

        elif secondint <= 0:
            await ctx.send("I can't do count negatives")

        else:
            message = await ctx.send(f"Timer: {seconds}")

            while True:
                secondint -= 1
                if secondint == 0:
                    await message.edit(content="Ended!")
                    break

                await message.edit(content=f"Timer: {secondint}")
                await asyncio.sleep(1)
    except ValueError:
        await ctx.send("You must enter a number!")



@bot.command()
async def invitelink(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=929424981690056734&permissions=8&scope=bot")


@bot.command()
async def info(ctx):
    text = "My name is Anos-Sama!\n I was built by Prince_Charming#8626. At present I have limited features(find out more by typing +help)\n :)"
    await ctx.send(text)  


@bot.command()
async def google(ctx,*, query):
		author = ctx.author.mention
		await ctx.channel.send(f"Here are the links related to your question {author} !")
		async with ctx.typing():
				for j in search(query, tld="co.in", num=1, stop=1, pause=2): 
						await ctx.send(f"\n:point_right: {j}")
				await ctx.send("Have any more questions:question:\nFeel free to ask again :smiley: !")

@bot.command()
async def serverinfo(ctx):
  members = len(ctx.guild.members)
  roles = len(ctx.guild.roles)
  x = discord.Embed(title='**Server Information:**',color = ctx.author.color)
  x.add_field(name='Name:', value=ctx.guild.name, inline=False)
  x.add_field(name='ID:', value=ctx.guild.id, inline=False)
  x.add_field(name='Owner:', value=ctx.guild.owner.mention, inline=False)
  x.add_field(name='start time:', value=ctx.guild.created_at.strftime('Date: %d/%m/%Y time: %H:%M:%S %p'), inline=False)
  x.add_field(name='Region:', value=ctx.guild.region, inline=False)
  x.add_field(name='Members:', value=f'`{members}`', inline=False)
  x.add_field(name=f'roles:', value=f'`{roles}`', inline=False)
  x.set_thumbnail(url=ctx.guild.icon_url)
  x.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
  x.timestamp = datetime.datetime.utcnow()
  await ctx.send(embed=x)


def roll_convert(argument):
    intarg = int(argument)
    switcher = {
        1: ":one:",
        2: ":two:",
        3: ":three:",
        4: ":four:",
        5: ":five:",
        6: ":six:",
        7: ":seven:",
        8: ":eight:",
        9: ":nine:",
        0: ":zero:"
    }
    return switcher.get(intarg, "what")

@bot.command()
async def roll(ctx):
    r = str(random.randrange(1, 101))
    mes = 'You number - '
    for m in r:
        mes += roll_convert(m)

    await ctx.send(mes)



@bot.command()
async def avatar(ctx, membro : discord.Member = 'nada'):
  if membro != 'nada':
    x = discord.Embed(title=f'Avatar of {membro.display_name}',description=f"[Download image]({membro.avatar_url})",color = ctx.author.color)
    x.set_image(url=membro.avatar_url)
    x.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=x)
  else:
    x = discord.Embed(title='Your avatar',description=f"[Download image]({ctx.author.avatar_url})" ,color = ctx.author.color)
    x.set_image(url=ctx.author.avatar_url)
    x.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=x)

          

extensions = [
	'cogs.cog_example'  # Same name as it would be if you were importing it
]

brains = [
    'cogs.chatbot'  
]

animes = [
    'cogs.anime'  
]

Utilities = [
    'cogs.cog_commands'  
]

if __name__ == '__main__':  # Ensures this is the file being ran
	for extension in extensions:
		bot.load_extension(extension)  # Loades every extension.
for brain in brains:
    bot.load_extension(brain)
for anime in animes:
    bot.load_extension(anime)
for Utility in Utilities:
    bot.load_extension(Utility)
keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET") 
bot.run(token)  # Starts the bot
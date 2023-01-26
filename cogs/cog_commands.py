import discord
from discord.ext import commands



class Utility(commands.Cog):
	'''These are the utilities commands'''

	def __init__(self, bot):
		self.bot = bot
    
	@commands.command()
	async def suggest(self, ctx, *, string_input):
		await ctx.message.delete()
		embed = discord.Embed(description=string_input, timestamp=ctx.message.created_at,color = ctx.author.color)
		embed.set_author(name=f"Suggestion by {ctx.message.author.display_name}", icon_url=ctx.message.author.avatar_url)
		msg = await ctx.send(embed=embed)
		await msg.add_reaction("👍")
		await msg.add_reaction("👎")
	
	@commands.command()
	async def ping(self, ctx):
		await ctx.send(embed=discord.Embed(title="Pong.",description=f"Anos-sama's current ping is **{round(self.bot.latency * 1000)}ms**",timestamp=ctx.message.created_at,color = ctx.author.color))





def setup(bot):
	bot.add_cog(Utility(bot))
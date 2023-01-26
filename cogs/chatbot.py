import discord
from discord.ext import commands
import requests

class Chat(commands.Cog):
	'''These are the chat bot commands'''

	def __init__(self, bot):
		self.bot = bot

	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.command()
	async def anos(self, ctx, *, msg: str = None):
		async with ctx.channel.typing():
			if msg == None:
				await ctx.send("Hello! In order to chat with me use: `+anos <message>`")
				return

			response = requests.get(f"http://api.brainshop.ai/get?bid=169954&key=2PbnxCY9JGH6olWj&uid={ctx.author.id}&msg={msg}").json()['cnt']

			await ctx.send(response)

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.bot:
			return

		if message.channel.id == None: # CHANNEL ID
			ctx = await self.client.get_context(message)
			await ctx.invoke(self.client.get_command('chat'), msg=message.content)

def setup(bot):
	bot.add_cog(Chat(bot))
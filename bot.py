import json
import discord
# File handling
f = open("secret.json")
secrets = json.load(f)

# Main MemberBox code
class MemberBox(discord.Client):
	# HELPER FUNCTIONS
	async def createBox(self, message):
		boxName = "Open Box"
		print(message)
		await message.channel.send(f"Box \'{boxName}\' created")

	async def closeBox(self, message):
		boxName = "Open Box"
		print(message)
		await message.channel.send(f"Box {boxName} closed: {AutoBox}")

	async def deleteBox(self, message):
		boxName = "Open Box"
		print(message)
		await message.channel.send(f"Box {boxName} created")

	# EVENT FUNCTIONS
	async def on_ready(self):
		print('Logged on as', self.user)

	async def on_message(self, message):
		# don't respond to ourselves
		if message.author.bot == True :
			return

		if message.content[:10] == 'MemberBox ':
			comand = message.content[10:]
			print()
			if comand == 'create-box':
				await self.createBox(message);
			elif comand == 'close-box':
				await self.closeBox(message)
			elif comand == 'delete-box':
				await self.deleteBox(message)
			else:
					await message.channel.send(f"The comand ```{comand}``` is not recognized for help. Try ```MemberBox -help for more information```")

# End of class

client = MemberBox()
client.run(secrets['bot_token'])
import json
import discord
# File handling
f = open("secret.json")
secrets = json.load(f)

# Main MemberBox code
class MemberBox(discord.Client):
	# Constructor
	def __init__(self):
		self.boxes = []
		self.isBoxOpen = False;
		super(MemberBox, self).__init__()

	# HELPER FUNCTIONS
	async def createBox(self, message, flags):
		boxName = 'Open Box'
		self.isBoxOpen = True;
		print(message)
		print(flags)
		await message.channel.send(f"Box \'{boxName}\' created")

	async def closeBox(self, message, flags):
		if self.isBoxOpen == False:
			await message.channel.send('There is no open box. Try opening a box with `MemberBox create-box`')
			return
		self.isBoxOpen = False;
		boxName = 'Open Box'
		NewBoxName = f'Box{len(self.boxes)}'
		print(message)
		print(flags)
		await message.channel.send(f'Box {boxName} closed: {NewBoxName}')

	async def deleteBox(self, message, flags):
		boxName = 'Open Box'
		print(message)
		print(flags)
		await message.channel.send(f'Box {boxName} destroyed')

	async def manageFlags(self, flags):
		print(flags)

	# EVENT FUNCTIONS
	async def on_ready(self):
		print('Logged on as', self.user)

	async def on_message(self, message):
		flags = []
		comand = ''
		# don't respond to ourselves
		if message.author.bot == True :
			return

		if message.content[:10] == 'MemberBox ':
			for i in message.content[10:].split(' '):
				if i[0] == '-':
					flags.append(i)
				else:
					comand = i
					break
			if comand == 'create-box':
				await self.createBox(message, flags)
			elif comand == 'close-box':
				await self.closeBox(message, flags)
			elif comand == 'delete-box':
				await self.deleteBox(message, flags)
			elif flags[0] != NULL:
				await self.manageFlags(flags)
			else:
					await message.channel.send(f'The comand ```{comand}``` is not recognized for help. Try ```MemberBox -help for more information```')

# End of class

client = MemberBox()
client.run(secrets['bot_token'])
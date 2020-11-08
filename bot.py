import json
import discord
# File handling
f = open("secret.json")
secrets = json.load(f)
f.close()

# Main MemberBox code
class MemberBox(discord.Client):
	# Constructor
	def __init__(self):
		self.boxes = [[]]
		self.openBox = 'Open Box-MB'
		self.openBoxes = []
		super(MemberBox, self).__init__()

	# HELPER FUNCTIONS
	def isBoxOpen(self, guild):
		for i in guild.roles:
			if str(i) == self.openBox:
				return True
		return False
	def lookupRoleID(self, target, guild):
		for role in guild.roles:
			print(role.id)

	async def createBox(self, message, flags):
		guild = message.author.guild
		if self.isBoxOpen(guild):
			await message.channel.send(f'The box {self.openBox}. Try closing the box first with `MemberBox close-box`')
			return
		print(self.isBoxOpen(guild))
		self.openBox = 'Open Box-MB'
		guild = message.author.guild
		newBox = await guild.create_role(name=self.openBox)
		self.openBoxes.append(newBox)
		print(message)
		print(flags)
		await message.channel.send(f"Box \'{self.openBox}\' created")

	async def closeBox(self, message, flags):
		guild = message.author.guild
		NBset = False
		# Makes sure there is an open box
		if not self.isBoxOpen(guild):
			await message.channel.send('There is no open box. Try opening a box with `MemberBox create-box`')
			return
		# Sets name of the new role
		if flags != None:
			for flag in flags:
				if flag[:3] == '-n\"' and flag[len(flag) - 1] == '\"':
					NewBoxName = f'{flag[3:len(flag)]}-MB'
					NBset = True
		if not NBset:
			NewBoxName = f'Box{len(self.boxes)}'
		# Creates the new role and saves the value
		guild = message.author.guild
		await guild.get_role(self.openBox).update(name=NewBoxName)
		newBox = NewBoxName
		self.boxes.append(newBox)
		await message.channel.send(f'Box {self.openBox} closed: {NewBoxName}')
		# Reset open box
		self.openBox = ''


	async def deleteBox(self, message, flags):
		boxName = ''
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
			elif flags[0] != None:
				await self.manageFlags(flags)
			else:
					await message.channel.send(f'The comand ```{comand}``` is not recognized for help. Try ```MemberBox -help for more information```')
	
	async def on_new_member_join(self, member):
		if self.isBoxOpen(guild) == True:
			await message.channel.send(self.openBox)

# End of class
client = MemberBox()
client.run(secrets['bot_token'])
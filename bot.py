import json
import discord
# File handling
f = open("secret.json")
secrets = json.load(f)
f.close()

# Main MemberBox code
class MemberBox(discord.Client):
	# Constructor
	def __init__(self, intents=discord.Intents().all()):
		# Name for the open box
		self.openBox = 'Open Box-MB'
		# Current Open boxes format { guild : role ID }
		self.openBoxes = {}
		super(MemberBox, self).__init__(intents=discord.Intents().all())

	# HELPER FUNCTIONS
	def isBoxOpen(self, guild):
		""" This function checks if the guild has an open box. If it doesn't the function creates one and stores it in openBoxes """
		for i in guild.roles:
			if str(i) == self.openBox:
				self.openBoxes[guild.name] = i
				return True
		return False

	def cache(self, g, role):
		"""Caches the given role's value into the json"""
		in_f = open("cache.json")
		cache = json.load(in_f)
		in_f.close()
		if not(str(g) in cache):
			cache.update({ str(g) : {str(role) : role.id} })
		else:
			cache[str(g)][str(role)] = role.id
		out_f = open("cache.json", 'w')
		cache = json.dump(cache, out_f)
		out_f.close()

	def createBoxId(self, g, s, i):
		"""Generates The ID for a given box"""
		flag = True
		in_f = open("cache.json")
		cache = json.load(in_f)
		in_f.close()
		if not (str(g) in cache):
			return f"Box {i}{s}"
		for value in cache[str(g)]:
			if value == f"Box {i}{s}":
				return self.createBoxId(g, s, i + 1)
			return f"Box {i}{s}"

	def getFromCache(self, k1, k2):
		"""Gets an id from the cache (k1=guild_name, k2=role_name)"""
		cache = {}
		rtn = -1
		f =  open('cache.json', 'r')
		cache = json.load(f)
		f.close()
		try:
			rtn = cache[k1][k2]
		except KeyError:
			pass
		if rtn != -1:
			del cache[k1][k2]
			out_f = open("cache.json", 'w')
			cache = json.dump(cache, out_f)
			out_f.close()
		
		return rtn

	# COMAND FUNCTIONS
	async def createBox(self, message, flags):
		"""The `create-box` command can be used to make a new box called `Open Box-MB`, while the box is open, anyone who joins is put into the box. Use `close-box` to end the open box period."""
		print(flags)
		for flag in flags:
			if flag == '-help':
				await self.manageHelp(self.createBox, message)
				return
		guild = message.author.guild
		if self.isBoxOpen(guild):
			await message.channel.send(f'The box `{self.openBox}` is open. Try closing the box first with `MemberBox close-box`')
			return
		self.openBox = 'Open Box-MB'
		guild = message.author.guild
		newBox = await guild.create_role(name=self.openBox)
		await message.channel.send(f"Box `{self.openBox}` created")

	async def closeBox(self, message, flags):
		"""The `close-box` command can be used to end the open box period. This makes it into a closed box that can later be removed with the `delete-box` command."""
		option = '-MB'
		guild = message.author.guild
		# Handles Flags
		for flag in flags:
			print(flag)
			if flag == '-help':
				await self.manageHelp(self.closeBox, message)
				return
			if flag[:3] == '-t\"' and flag[len(flag) - 1] == '\"':
				option = f': {flag[3 : len(flag) - 1]}-MB'
				NBset = True
			elif flag[:3] == '-t\"':
				await message.channel.send('ERROR: Spaces are not allowed in your tag (-t)')
				return
		# Makes sure there is an open box
		if not self.isBoxOpen(guild):
			await message.channel.send('There is no open box. Try opening a box with `MemberBox create-box`')
			return
		NewBoxName = self.createBoxId(guild, option, 1)
		# Creates the new role and saves the value
		await self.openBoxes[guild.name].edit(name=NewBoxName)
		self.cache(guild, self.openBoxes[guild.name])
		await message.channel.send(f'Box {self.openBox} closed: {NewBoxName}')

	async def deleteBox(self, message, flags):
		"""The `delete-box` command can be used to destroy a given box. Enter `Memberbox delete-box [name of box]` to get rid of a given box, this will remove all people in the box from the sever."""
		for flag in flags:
			if flag == '-help':
				await self.manageHelp(self.deleteBox, message)
				return
		guild = message.author.guild
		lst = message.content.split(" ")
		# Get the box from the message
		target = ''
		lst =  [l for l in lst if l]
		if lst[len(lst) - 1] == 'delete-box':
			await message.channel.send('ERROR: Enter the box you want deleted after `delete-box`')
		for i in range(len(lst)):
			if lst[i] == 'delete-box':
				try:
					while lst[i][len(lst[i]) - 3:] != '-MB':
						i += 1
						target += lst[i] + ' '
						break
				except:
					pass
		target = target[:len(target) - 1]
		boxKey = self.getFromCache(str(guild),target)
		if boxKey == -1:
			await message.channel.send(f'ERROR: The Box {target} could not be found')
			return
		# Destroy the box
		for user in guild.get_role(boxKey).members:
			await guild.kick(user)
		await guild.get_role(boxKey).delete()
		await message.channel.send(f'Box `{target}` destroyed')

	async def manageHelp(self, source, message):
		"""Sends a message for the help flag"""
		await message.channel.send(source.__doc__)


	# EVENT FUNCTIONS
	async def on_ready(self):
		print('Logged on as', self.user)

	async def on_message(self, message):
		""" Welcome to MemberBox, To create a box use `MemberBox create-box`.
		
		Use `MemberBox close-box` to seal it. The Flag `-t"tag"` can be used to assign a tag to the Box.
		
		`delete-box [Box Name]` will remove a box and all of it's members.
		"""
		print(message)
		print(message.content)
		flags = []
		in_str = False
		comand = ''
		# don't respond to ourselves
		if message.author.bot == True :
			return

		if message.content[:10] == 'MemberBox ':
			for i in message.content[10:].split(' '): 
				if i != '' and i[0] == '-':
					flags.append(i)
				else:
					if comand == '':
						comand = i
					else:
						break			# THROW ERROR HERE TO MANY COMANDS
			if comand == 'create-box':
				await self.createBox(message, flags)
			elif comand == 'close-box':
				await self.closeBox(message, flags)
			elif comand == 'delete-box':
				await self.deleteBox(message, flags)
			elif flags != None:
				for flag in flags:
					if flag == '-help':
						await self.manageHelp(self.on_message, message)
			else:
					await message.channel.send(f'The comand ```{comand}``` is not recognized for help. Try ```MemberBox -help for more information```')
	
	async def on_member_join(self, member):
		guild = member.guild
		if self.isBoxOpen(guild) == True:
			guild = member.guild
			cur_box = self.openBoxes[guild.name]
			await member.add_roles(cur_box)

# End of class
client = MemberBox()
client.run(secrets['bot_token'])
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
		self.openBox = 'Open Box-MB'
		self.openBoxes = {}
		super(MemberBox, self).__init__(intents=discord.Intents().all())

	# HELPER FUNCTIONS
	def isBoxOpen(self, guild):
		for i in guild.roles:
			if str(i) == self.openBox:
				self.openBoxes[guild.name] = i
				return True
		return False

	def cache(self, g, role):
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
		guild = message.author.guild
		if self.isBoxOpen(guild):
			await message.channel.send(f'The box `{self.openBox}` is open. Try closing the box first with `MemberBox close-box`')
			return
		print(self.isBoxOpen(guild))
		self.openBox = 'Open Box-MB'
		guild = message.author.guild
		newBox = await guild.create_role(name=self.openBox)
		print(message)
		print(flags)
		await message.channel.send(f"Box \'{self.openBox}\' created")

	async def closeBox(self, message, flags):
		option = '-MB'
		guild = message.author.guild
		# Makes sure there is an open box
		if not self.isBoxOpen(guild):
			await message.channel.send('There is no open box. Try opening a box with `MemberBox create-box`')
			return
		# Sets name of the new role
		# Flags are broken
		if flags != None:
			for flag in flags:
				print(flag)
				if flag[:3] == '-t\"' and flag[len(flag) - 1] == '\"':
					option = f': {flag[3 : len(flag) - 1]}-MB'
					NBset = True
				elif flag[:3] == '-t\"':
					await message.channel.send(' Spaces are not allowed in your tag (-t)')
		NewBoxName = self.createBoxId(guild, option, 1)
		# Creates the new role and saves the value
		await self.openBoxes[guild.name].edit(name=NewBoxName)
		self.cache(guild, self.openBoxes[guild.name])
		await message.channel.send(f'Box {self.openBox} closed: {NewBoxName}')

	async def deleteBox(self, message, flags):
		guild = message.author.guild
		lst = message.content.split(" ")
		# Get the box from the message
		target = ''
		for i in lst:
			if i == '':
				lst.remove(i)
		if lst[len(lst) - 1] == 'delete-box':
			await message.channel.send('Specify the box you want deleted after `delete-box`')
		for i in range(len(lst)):
			if lst[i] == 'delete-box':
				while lst[i][len(lst[i]) - 3:] != '-MB':
					i += 1
					try:
						target += lst[i] + ' '
					except:
						pass
				break
		target = target[:len(target) - 1]
		boxKey = self.getFromCache(str(guild),target)
		if boxKey == -1:
			await message.channel.send(f'The Box {target} could not be found')
			return
		# Destroy the box
		for user in guild.get_role(boxKey).members:
			await guild.kick(user)
		await guild.get_role(boxKey).delete()
		await message.channel.send(f'Box `{target}` destroyed')

	async def manageHelp(self, source, message, flags):
		guild = message.author.guild
		for value in flags:
			if value == '-help': 
				await message.channel.send(source.__doc__)
		print(flags)

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
				await self.manageHelp(self.on_message, message, flags)
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
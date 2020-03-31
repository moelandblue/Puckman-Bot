import json
import os
import discord
from discord.ext import commands

from Leaderboards import Leaderboards
from Weather import Weather
from Administration import Administration

settings = {}


def get_prefix(client, message):
	return settings[str(message.guild.id)]["prefix"]


puckman = commands.Bot(command_prefix=get_prefix)

# Extensions
puckman.add_cog(Leaderboards(puckman))
puckman.add_cog(Weather(puckman))
puckman.add_cog(Administration(puckman))

# Overwrite
puckman.remove_command("help")


@puckman.event
async def on_ready():
	"""
	Load state and update information since last run
	"""
	await load_state()
	await puckman.change_presence(activity=discord.Game(name="Ice Hockey"))
	await update_guilds(puckman)

	print("Logged on as {0}".format(puckman.user))


async def load_state():
	global settings

	with open(os.path.join("config", "settings.json"), "r+") as settingsFile:
		settings = json.loads(settingsFile.read())


async def update_state():
	global settings

	with open(os.path.join("config", "settings.json"), "r+") as settingsFile:
		settingsFile.truncate(0)
		settingsFile.seek(0)
		json.dump(settings, settingsFile, indent=4)


@puckman.command(pass_context=True)
async def help(ctx):
	"""
	Sends help information
	"""

	helpEmbed = discord.Embed(title="Puckman Bot", colour=discord.Colour.red())
	helpEmbed.add_field(name="Documentation", value="https://samuelcurrid.github.io/Puckman-Bot/documentation.html")
	helpEmbed.set_thumbnail(url="https://raw.githubusercontent.com/moelandblue/Puckman-Bot/master/assets/puckman.png")
	helpEmbed.set_footer(text="Source: https://github.com/moelandblue/Puckman-Bot")

	await ctx.message.channel.send(embed=helpEmbed)


async def update_guilds(self):
	"""
	Updates guilds included in leaderboards.json
	"""
	global settings

	savedGuilds = []
	for guildID in settings:
		savedGuilds.append(int(guildID))

	guilds = []
	for guild in puckman.guilds:
		guilds.append(guild.id)

	addGuilds = [x for x in guilds if x not in savedGuilds]
	removeGuilds = [x for x in savedGuilds if x not in guilds]

	# Add new guilds
	for guildID in addGuilds:
		settings[str(guildID)] = {"prefix": "."}

	# Remove disconnected guilds
	for guildID in removeGuilds:
		settings.pop(str(guildID))

	await update_state()


@puckman.command(pass_context=True, name="prefix")
async def change_prefix(ctx, prefix):
	if ctx.message.author.guild_permissions.administrator:
		settings[str(ctx.message.guild.id)]["prefix"] = str(prefix)

		await update_state()


puckman.run(json.load(open(os.path.join("config", "tokens.json")))["testToken"])

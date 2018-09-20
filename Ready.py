import discord
from discord.ext import commands
import asyncio

BotToken = "BOT TOKEN" #TODO Replace with bot token
serverID = 0000000000 #TODO Replace with the serverID
ChanId = 00000000000 #TODO Replace with the channelID

# Variables
version = "v3.0"
rdyCheck = False
vChannel = "ready-check"
rRole = "Officers"
count = 0
rdyUsers = ""

# Create Bot
bot = commands.Bot(command_prefix='!', description='A bot to check if members are available to participate')




@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.remove_command('help')


@bot.command()
async def help(ctx):
    channel = str(ctx.message.channel.name)
    if channel == vChannel:
        embed = discord.Embed(title="Commands", description="A list of bot commands", color=0xeee657)

        # Info Command
        embed.add_field(name="!info", value="Information on current version changes", inline=False)

        # Ready Up Command
        embed.add_field(name="!R <role>", value="Starts a ready check. Can only be started by an Officer")

        # Ready Command
        embed.add_field(name="!rdy", value="Indicates that you are ready to participate. Can only be used for "
                                           " 60 seconds after an officer has used the ready up command.")
        # Footer
        embed.set_footer(text="Version " + version)

        await ctx.send(embed=embed)


@bot.command()
async def info(ctx):
    channel = str(ctx.message.channel.name)
    if channel == vChannel:
        embed = discord.Embed(title="Ready Check", description="A bot for ready checks", color=0xeee657)

        # Personal Info
        embed.add_field(name="Author", value="OakNLeaf")

        # Version Info
        embed.add_field(name="Version", value=version)

        # Version Changes
        embed.add_field(name=version + " changes", value="Lists all users that indicated they were ready")

        # Footer
        embed.set_footer(text="Version " + version)

        await ctx.send(embed=embed)


@bot.command()
@commands.has_role(rRole)
async def R(ctx, memberRole: str, dm: bool = False):
    global count
    global rdyCheck
    global rdyUsers
    channel = str(ctx.message.channel.name)
    if channel == vChannel:
        if rdyCheck:
            await ctx.send("A rdyCheck is already taking place, please wait for it to finish before starting a new one")
            return
        role = discord.utils.get(ctx.guild.roles, name=memberRole)
        server = bot.get_guild(serverID)
        if dm:
            for member in server.members:
                if discord.utils.get(member.roles, name=memberRole) is not None:
                    try:
                        await member.send(role.mention + ", " + ctx.message.author.mention + " has initiated a ready "
                                                                                             "check.Please respond with"
                                                                                             " !rdy in the #ready-check"
                                                                                             " channel")
                    except:
                        await ctx.send("Failed to message" + str(member.display_name))
        else:
            await ctx.send(role.mention + ", " + ctx.message.author.mention + " has initiated a ready check. Please"
                                                                              " respond with !rdy in the"
                                                                              " #ready-check channel")
        rdyUsers = ""
        rdyCheck = True
        count = 0
        await asyncio.sleep(60)
        if count > 1:
            await ctx.send(str(count) + " members have indicated that they are ready:")
        elif count == 0:
            await ctx.send("Nobody indicated that they are ready.")
        else:
            await ctx.send("Only one person indicated that they were ready:")
        if count > 0:
            await ctx.send(rdyUsers)
        rdyCheck = False
        count = 0


@bot.command()
async def rdy(ctx):
    global count
    global rdyCheck
    global rdyUsers
    if rdyCheck:
        count = count + 1
        rdyUsers = rdyUsers + str(ctx.message.author.display_name) + "(ready)\n"
        await ctx.send(str(ctx.message.author.display_name) + " is ready")
    else:
        await ctx.send("A rdycheck has not been started or has already been completed")


@bot.command()
async def update_message(ctx):
    channel = bot.get_channel(ChanId)
    if channel == vChannel:
        embed = discord.Embed(title="New Update", description="Version " + version + " is now live", color=0xeee657)
        embed.add_field(name="Changes for current version:", value="!R has been updated to allow the command to dm members"
                                                               " directly or to mention the role in the channel when"
                                                               " a rdyCheck is initiated.")
        embed.add_field(name="!R <role> T", value="Sends a direct message to all members of indicated role")

        embed.add_field(name="!R <role>", value="Mentions the indicated role in the channel")

        embed.set_footer(text="Version " + version)
        await ctx.send(embed=embed)

bot.run(BotToken)

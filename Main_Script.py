from tabnanny import check
import lightbulb
import hikari
import spreadsheet as sheet

bot = lightbulb.BotApp(token='MTA3OTE5NTA5NzkxODM0OTM2Mg.G5hF-j.B4nPXW58qEvd80kjhslYwsRPRnFJTW4bvxnvZY', intents=hikari.Intents.ALL)
errorImage = "https://i.imgur.com/M4rnmDX.gif"
successImage = "https://i.imgur.com/Mzh3ZVE.gif"
modId = 1048742410890526851

@bot.listen(hikari.GuildMessageCreateEvent)
async def message(event):
    if not event.is_bot and event.content == "test":
        await bot.rest.create_message(event.channel_id, "copy")

    if not event.is_bot and event.content == "who is a simp":
        await bot.rest.create_message(event.channel_id, "John Cha", tts=True)

    if not event.is_bot and event.content == "tell me a fact":
        await bot.rest.create_message(event.channel_id, "John is a simp", tts=True)

    if not event.is_bot and event.content == "what should i do":
        await bot.rest.create_message(event.channel_id, "Study you little bitch", tts=True)

    if not event.is_bot and event.content == "fuck you":
        await bot.rest.create_message(event.channel_id, "You want to?", tts=True)
    
@bot.command
@lightbulb.option('month', "Numerical birth month", type=int)
@lightbulb.option('day', "Numerical birth date", type=int)
@lightbulb.command('bday', 'Add your birthdate')
@lightbulb.implements(lightbulb.SlashCommand)
#adds birthdate user info on google sheets
#adds user guild info on google sheets
async def bday(ctx):
    embed = hikari.Embed(title="Success", description="Birthdate saved")
    embed.set_thumbnail(successImage)
    
    day = ctx.options.day
    month = ctx.options.month
    userId = ctx.author.id
    guildId = ctx.guild_id
    
    check1 = await check_date(day, month, ctx)
    check2 = await check_guild(ctx)

    if not check1 or not check2:
        return
    
    sheet.NewUser(day, month, userId)
    sheet.NewDate(day, month, userId)
    await ctx.respond(embed)

#returns false if day and month are invalid 
async def check_date(day, month, ctx):
    embed = hikari.Embed(title="Error", description="Enter valid date")
    embed.set_thumbnail(errorImage)

    day = int(day)
    month = int(month)
    if day > 31 or day < 0 or month > 12 or month < 0:
        await ctx.respond(embed)
        return False
    return True

async def check_guild(ctx):
    embed = hikari.Embed(title="Error", description="Server not set up")
    embed.set_thumbnail(errorImage)

    guildId = sheet.GetGuild()
    if not guildId:
        await ctx.respond(embed)
        return False
    return True

@bot.command
@lightbulb.option('channelid', "Enter channel ID")
@lightbulb.command('setup', 'set new channel')
@lightbulb.implements(lightbulb.SlashCommand)
#ties the guild to a channel
async def setup(ctx):
    embed = hikari.Embed(title="Success", description="Channel set")
    embed.set_thumbnail(successImage)

    channelId = ctx.options.channelid
    guildId = ctx.guild_id

    check1 = await check_channel(ctx, channelId)
    
    if check1:
        sheet.NewGuild(guildId)
        sheet.NewChannel(channelId)
        await ctx.respond(embed)

async def check_channel(ctx, channelId):
    embed = hikari.Embed(title="Error", description="Channel not found in server")
    embed.set_thumbnail(errorImage)

    guildId = ctx.guild_id
    channels_in_guild = bot.cache.get_guild_channels_view_for_guild(guildId).keys()
    channelLst = [i for i in channels_in_guild]
    if not int(channelId) in channelLst:
        await ctx.respond(embed)
        return False
    return True

@bot.command
@lightbulb.command('remove', 'remove your birthdate')
@lightbulb.implements(lightbulb.SlashCommand)
async def remove(ctx):
    embed = hikari.Embed(title="Success", description="Birthdate removed")
    embed.set_thumbnail(successImage)
    embed2 = hikari.Embed(title="Error", description="User not found")
    embed2.set_thumbnail(errorImage)

    userId = ctx.author.id
    found = sheet.ClearUser(userId)

    if not found:
        await ctx.respond(embed2)
    else:    
        await ctx.respond(embed)

@bot.command
@lightbulb.add_checks(lightbulb.has_roles(modId))
@lightbulb.option('userid', 'Enter user id')
@lightbulb.command('oremove', 'remove user birthdate')
@lightbulb.implements(lightbulb.SlashCommand)
async def oremove(ctx):
    embed = hikari.Embed(title="Success", description="Birthdate removed")
    embed.set_thumbnail(successImage)
    embed2 = hikari.Embed(title="Error", description="User not found")
    embed2.set_thumbnail(errorImage)

    userId = ctx.author.id
    found = sheet.ClearUser(userId)

    if not found:
        await ctx.respond(embed2)
    else:
        await ctx.respond(embed)
        
@bot.listen(lightbulb.CommandErrorEvent)
async def onError(event):
    embed = hikari.Embed(title="Error", description="Must be a moderator")
    embed.set_thumbnail(errorImage)
    
    if isinstance(event.exception, lightbulb.errors.MissingRequiredRole):
        await event.context.respond(embed)
        
#when almost done, prevent duplicates
bot.run()
import discord
from discord.ext import commands

# Token

TOKEN = ''


# Prefix

mercury = commands.Bot(command_prefix='/')


# Startup / Status

@mercury.event
async def on_ready():
    print('Mercury is now online.')
    await mercury.change_presence(activity=discord.Game('Mercury'))


# Ping

@mercury.command()
async def ping(ctx):
    embed = discord.Embed(title='Ping', description=f'The ping is currently {round(mercury.latency * 1000)}ms.', color=discord.Color.dark_gray())
    await ctx.send(embed=embed)


# Suggestion / Poll / Update / Announcement

@mercury.command()
async def suggestion(ctx, *, description):
    embed = discord.Embed(title='__Suggestion__', description=f'', color=discord.Color.dark_gray())
    embed.set_footer(text=f'Suggested by - {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.add_field(name='Description', value=description)
    channel = ctx.guild.get_channel()  # <------- Put the Suggestions channel ID inside the brackets.
    msg = await channel.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')


@mercury.command()
@commands.has_permissions(administrator=True)
async def poll(ctx, *, message):
    embed = discord.Embed(title=f'__Poll__', color=discord.Color.dark_gray())
    embed.set_footer(text=f'Created by - {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.add_field(name='Description', value=f'{message}', inline=False)
    channel = ctx.guild.get_channel()  # <------- Put the Poll channel ID inside the brackets.
    msg = await channel.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')


@mercury.command()
@commands.has_permissions(administrator=True)
async def announcement(ctx, *, message):
    embed = discord.Embed(title=f'**__Announcement__**', color=discord.Color.dark_gray())
    embed.set_footer(text=f'Announced by - {ctx.author}', icon_url=ctx.author.avatar_url)
    embed.add_field(name='Description:', value=f'{message}', inline=False)
    channel = ctx.channel.send()  # <------- Put the Announcements channel ID inside the brackets.
    await ctx.send(embed=embed)


@mercury.command()
@commands.has_permissions(administrator=True)
async def update(ctx, *, description):
    embed = discord.Embed(title='__Update__', description=f' ', color=discord.Color.dark_gray())
    embed.add_field(name='Description', value=description)
    channel = ctx.guild.get_channel()  # <------- Put the Updates/Changelog channel ID inside the brackets.
    await ctx.send(embed=embed)


# Lockdown /  Unlock

@mercury.command()
@commands.has_permissions(administrator=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + ' is now in lockdown.')


@mercury.command()
@commands.has_permissions(administrator=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + ' is now unlocked.')


# Clear / Slowmode

@mercury.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    if amount is None:
        await ctx.channel.purge(limit=1000000)
    else:
        await ctx.channel.purge(limit=amount)


@mercury.command()
@commands.has_permissions(administrator=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f'Slowmode has been enabled, you can talk every {seconds} seconds.')


# Ban / Mute / Kick

@mercury.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    embed = discord.Embed(title='__Ban__', description=f'{member.mention} has been banned by {ctx.author.mention}', color=discord.Color.dark_gray())
    embed.add_field(name='Reason:', value=reason, inline=False)
    await ctx.send(embed=embed)


@mercury.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, reason=None):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.add_roles(role)
    embed = discord.Embed(title='__Mute__', description=f'{member.mention} has been muted by {ctx.author.mention}', color=discord.Color.dark_gray())
    embed.add_field(name='Reason:', value=reason, inline=False)
    await ctx.send(embed=embed)


@mercury.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(title='__Kick__', description=f'{member.mention} has been kicked by {ctx.author.mention}', color=discord.Color.dark_gray())
    embed.add_field(name='Reason:', value=reason, inline=False)
    await ctx.send(embed=embed)


# Run

mercury.run(TOKEN)

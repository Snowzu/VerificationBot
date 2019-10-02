import discord
from discord.ext import commands

# Put your prefered prefix
client = commands.Bot(command_prefix='YOUR_PREFIX_HERE')

# Logging into the bot
@client.event
async def on_ready():
    print(f'Logged in as {client.user}.\n-----------')


# When a new member joins, a role will be given to them.
@client.event
async def on_member_join(member):
    unverified = discord.utils.get(member.guild.roles, name="UNVERIFIED_ROLE_NAME_HERE")
    await member.add_roles(unverified)
    

def is_channel(ctx):
    return ctx.channel.id == VERIFICATION_CHANNEL_ID


# Command to verify a user.
@client.command()
@commands.check(is_channel)
async def verify(ctx):
    unverified = discord.utils.get(ctx.guild.roles, name="UNVERIFIED_ROLE_NAME_HERE")
    if unverified in ctx.author.roles:
        verify = discord.utils.get(ctx.guild.roles, name="VERIFIED_ROLE_NAME_HERE")
        msg = await ctx.send('Verification has been sent in DMs')
        await msg.add_reaction('✅')
        e = discord.Embed(color=0x7289da)
        e.add_field(name='Please complete the captcha below to gain access to the server.',
                    value='**NOTE:** This is **Case and Space Sensitive**')
        e.set_image(url='CAPTCHA_DISCORD_URL')
        await ctx.author.send(embed=e)

        def check(m):
            return m.content == 'CAPTCHA_RESPONSE'

        msg = await client.wait_for('message', check=check)
        e = discord.Embed(color=0x7289da)
        await ctx.author.remove_roles(unverified)
        e.add_field(name='Thank you for verifying!', value='You now have access to the server.')
        await ctx.author.send(embed=e)
        await ctx.author.add_roles(verify)
    else:
        await ctx.send('You are already verified!')
        

# Put your token here        
client.run('YOUR_TOKEN_HERE')

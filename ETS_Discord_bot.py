import discord
from discord.ext import commands, tasks
from better_profanity import profanity
from collections import defaultdict
from datetime import timedelta
import asyncio

TOKEN = 'botTokenHere'  # Replace with your bot's token

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.guilds = True
intents.message_content = True  # Enable the message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

profanity_violations = defaultdict(int)

ROLE_NAME = 'Member'  # The role to assign
TIMEOUT_ROLE_NAME = 'Timeout'
RULES_MESSAGE_ID = 0123456789  # Replace with your rules message ID
RULES_CHANNEL_ID = 0123456789  # Replace with your rules channel ID
REACTION_EMOJI = '✅'  # The emoji users should react with

OFFICERS_USER_IDS = [00000000000] #Replace with officer user ID

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    profanity.load_censor_words()


@bot.event
async def on_member_join(member):
    print(f"New member joined: {member}")
    role_id = 000000000  # Replace with the actual role ID
    role = member.guild.get_role(role_id)
    if role:
        await member.add_roles(role)
        print(f"Assigned role {role.name} to {member.name}")
    else:
        print("Role not found")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == RULES_MESSAGE_ID and str(payload.emoji) == REACTION_EMOJI:
        guild = bot.get_guild(payload.guild_id)
        if guild:
            member_role = discord.utils.get(guild.roles, name="Member")
            unverified_role = discord.utils.get(guild.roles, name="Unverified")
            member = guild.get_member(payload.user_id)

            if member and not member.bot:
                # Add the 'Member' role
                if member_role:
                    await member.add_roles(member_role)
                    print(f"Assigned 'Member' role to {member.name}")

                # Remove the 'Unverified' role if the member has it
                if unverified_role and unverified_role in member.roles:
                    await member.remove_roles(unverified_role)
                    print(f"Removed 'Unverified' role from {member.name}")
                else:
                    print("Either 'Unverified' role not found or the user doesn't have it")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    profanity.load_censor_words()

                    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if profanity.contains_profanity(message.content):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, your message was removed because it violates server guidelines.")
        
        # Increment the user's violation count
        profanity_violations[message.author.id] += 1

        # Apply a timeout role at 3 violations
        if profanity_violations[message.author.id] == 3:
            timeout_role = discord.utils.get(message.guild.roles, name=TIMEOUT_ROLE_NAME)
            if timeout_role:
                await message.author.add_roles(timeout_role)
                print(f"Assigned 'Timeout' role to {message.author.name}")
                try:
                    await message.author.send(f"You have been timed out for 24 hours due to repeated profanity violations.")
                except discord.errors.Forbidden:
                    print(f"Could not send DM to {message.author.name}")

                # Schedule to remove the timeout role after 24 hours
                await asyncio.sleep(24 * 60 * 60)  # 24 hours
                await message.author.remove_roles(timeout_role)
                print(f"Removed 'Timeout' role from {message.author.name}")

        # Notify officers and apply a longer timeout role at 5 violations
        if profanity_violations[message.author.id] == 5:
            notification_message = f"{message.author.mention} has reached 5 profanity violations."
            for officer_id in OFFICERS_USER_IDS:
                officer = await bot.fetch_user(officer_id)
                if officer:
                    await officer.send(notification_message)

            try:
                timeout_role = discord.utils.get(message.guild.roles, name=TIMEOUT_ROLE_NAME)
                if timeout_role:
                    await message.author.add_roles(timeout_role)
                    print(f"Assigned 'Timeout' role to {message.author.name}")
                    try:
                        await message.author.send(f"You have been timed out for 24 hours due to repeated profanity violations.")
                    except discord.errors.Forbidden:
                        print(f"Could not send DM to {message.author.name}")

                    # Schedule to remove the timeout role after 24 hours
                    await asyncio.sleep(24 * 60 * 60)  # 24 hours
                    await message.author.remove_roles(timeout_role)
                    print(f"Removed 'Timeout' role from {message.author.name}")
            except discord.errors.Forbidden:
                print(f"Bot does not have permission to manage roles for {message.author.name}")

    await bot.process_commands(message)
    
@bot.event
async def on_ready():
    global invites
    invites = {}
    for guild in bot.guilds:
        guild_invites = await guild.invites()
        invites[guild.id] = {invite.code: invite for invite in guild_invites}

async def get_used_invite(guild):
    global invites
    new_invites = await guild.invites()
    for invite in new_invites:
        if invite.code in invites[guild.id] and invite.uses > invites[guild.id][invite.code].uses:
            invites[guild.id][invite.code] = invite
            return invite
    return None


@bot.event
async def on_member_join(member):
    used_invite = await get_used_invite(member.guild)
    if used_invite:
        # Check if the used invite is the specific one for "Recruitment"
        if used_invite.code == "kgSEWM9dvV":  # Replace with your specific invite code
            recruitment_role = discord.utils.get(member.guild.roles, name="Recruitment")
            if recruitment_role:
                await member.add_roles(recruitment_role)
                print(f"Assigned 'Recruitment' role to {member.name}")
            else:
                print("Recruitment role not found")

    
@bot.command(name='profanitycount')
async def profanity_counts(ctx):
    if not profanity_violations:
        await ctx.send("No profanity violations recorded yet.")
        return

    message = "Profanity Violations:\n"
    for user_id, count in profanity_violations.items():
        user = await bot.fetch_user(user_id)
        user_name = user.name if user else f"UserID: {user_id}"
        message += f"{user_name}: {count}\n"

    await ctx.send(message)


@bot.command(name='socials')
async def resources(ctx):
    message = (
        "ETS Social Media Accounts!!:\n"
        "- [Instagram]()\n"
        "- [Facebook]()\n"
        "- [Website]()\n"
    )
    await ctx.send(message)

@bot.command(name='tutoring')
async def tutoring_schedule(ctx):
    schedule = "Tutoring Schedule:\n- Monday: During Both Lunches @Library & After School until 4:30 @Annex Rm #6\n- Tuesday: After School until 4:30 @Annex Rm #6"
    await ctx.send(schedule)

@bot.command(name='contact')
async def contact_info(ctx):
    contact_info = "Contact Information:\n \n- \n- Discord: Username\n- Phone #: "
    await ctx.send(contact_info)


bot.run(TOKEN)

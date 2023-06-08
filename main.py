import discord
import os
from discord.ext import commands
import signal
from keepalive import keep_alive
import re

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
paskey = os.environ['Paskey_nuke']

bot = commands.Bot(command_prefix='/', intents=intents)
token = os.environ['bot_token_justwait']

output = ""

def sort_members_by_number(output, channel):
    categories = re.findall(r'(\w+:)\n', output)  # Find all category names followed by a colon
    sorted_output = output
    for category in categories:
        start_index = sorted_output.index(category) + len(category)  # Find the start index of each category
        end_index = len(sorted_output)  # Initialize the end index with the length of the output
        next_category_index = sorted_output.find('\n\n', start_index)  # Find the start index of the next category

        if next_category_index != -1:
            end_index = next_category_index

        category_members = sorted_output[start_index:end_index].strip()  # Get the members belonging to the category
        sorted_members = re.findall(r'\[(\w+-\d+)\] ([^\n]+)', category_members)  # Find all members with their numbers
        sorted_members.sort(key=lambda member: int(member[0].split('-')[1]))  # Sort members based on the number

        # Replace the unsorted members with the sorted members in the output
        sorted_output = sorted_output[:start_index] + '\n'.join(
            f"[{member[0]}] {member[1]}" for member in sorted_members
        ) + sorted_output[end_index:]

        # Add a line break after each category
        sorted_output = sorted_output.replace(category, category + '\n')
    return sorted_output

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    global output  # Die global-Anweisung hier platzieren
    
    if message.author == bot.user:
        return
    if message.channel.name == "taggy-caller":
        channel1 = bot.get_channel(1113447646653325342)
        if message.content.startswith('/update'):
            await channel1.send("[1/2] start update...")
            server = bot.get_guild(1052277604197085255)
            await server.chunk()
            role_members = {}
            for member in server.members:
              if not member.bot:
                  roles = [role for role in member.roles][::-1]
                  for i in range(len(roles) - 1):
                      if "Division" in roles[i].name:
                          next_role = roles[i + 1]
                          if next_role.name not in role_members:
                              role_members[next_role.name] = []
                          role_members[next_role.name].append(member.display_name)  # Änderung hier
                          break
                        
            output = ""  # output hier deklarieren und initialisieren
            for role, members in role_members.items():
                if role not in ["@everyone", "╠═══════╡Erfolge╞═══════╣", "Regelwerk eingewilligt"]:
                    output += f"{role}:\n"
                    for member in members:
                        output += f"@{member}\n"  # Änderung hier
                    output += "\n"
            await channel1.send("[2/2] Liste erstellt...")
                  
            output = sort_members_by_number(output, channel1)  # output hier sortieren
            channel = bot.get_channel(1052597358690586736)
            async for old_message in channel.history(limit=200):
                if old_message.author == bot.user:
                    await old_message.delete()
                  
            await channel1.send("[+] Erfolgreich")
            await channel.send(output)

        if message.content.startswith('/force-stop'):
            current_pid = os.getpid()
            os.kill(current_pid, signal.SIGKILL)


keep_alive()
bot.run(token)

# LICENSE = MIT JustWait 2023
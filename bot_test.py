import discord
from dotenv import load_dotenv
import os
import datetime

TOKEN = os.getenv('TOKEN')
USERS = os.getenv('USERS')
SKIP = os.getenv('SKIP')
intents = discord.Intents.default()
intents.message_content = True
intents.members = False

bot = discord.Client(intents=intents)
# FILE_PATH = "./chat_logs/"
FILE_PATH = "./bwsi_logs/"

LOGGING = False


def log(*args, **kwargs):
    if LOGGING:
        print(*args, **kwargs)


def remove_short_files(directory):
    """Removes files with less than 2 lines from a given directory.

    Args:
      directory: The path to the directory to process.
    """

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    line_count = len(f.readlines())
                    if line_count < 2:
                        os.remove(file_path)
                        print(f"Removed {file_path}")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")


@bot.event
async def on_ready():
    for guild in bot.guilds:
        log(f"{guild.id} name: {guild.name}")


@bot.event
async def on_message(msg):
    channels = []
    channel_msgs = {}
    if msg.content == "hello":
        await msg.channel.send("test")
    if msg.content == "scan":
        for guild in bot.guilds:
            log(f"{guild.id} name: {guild.name}")
            for channel in guild.channels:
                channels.append(channel)
        log(f"\n\n\n{channels}")
    # <Message id=1263125889642663967 channel=<TextChannel id=1262959409064317071 name='general' position=0 nsfw=False news=False category_id=1262959409064317069> type=<MessageType.default: 0> author=<Member id=1262958127532474440 name='TonySARk - IronBeaver' global_name=None bot=True nick=None guild=<Guild id=1262959409064317068 name='Testing Grounds' shard_id=0 chunked=False member_count=2>> flags=<MessageFlags value=0>>,
    for channel in channels:
        if type(channel) == discord.channel.TextChannel:
            members = channel.members
            for member in members:
                if member.id == 1262958127532474440:
                    log("True")
                    log(f"Channel: {channel.name} \n Type: {type(channel)}")
                    messages = [message async for message in channel.history(limit=None)]
                    # print(messages)
                    channel_msgs[channel.name] = messages
    text_for_file = {}
    for channel_msg in channel_msgs.values():
        log("#"*50)
        log(type(channel_msg))
        log(channel_msg)
        log("#"*50)
        for message in channel_msg:
            user = message.author
            msg_id = message.id
            channel = message.channel
            text = message.content
            date = message.created_at
            date_formatted = date.ctime()

            if channel.name in SKIP or user.name in SKIP:
                log(f"In channel {message.channel} {user} sent message with id of {msg_id} on {date}:\n{text}")
            else:
                if user in text_for_file.keys():
                    text_for_file[user].append(
                        (user.name, channel, text, date_formatted))
                else:
                    text_for_file[user] = [
                        (user.name, channel, text, date_formatted)]

                for user in text_for_file:
                    log(user.display_name)
                    log(text_for_file[user])
                    if user.name == USERS[channel.name]:
                        file_name = FILE_PATH + \
                            str(message.channel) + "_" + str(user) + ".txt"
                        file = open(file_name, "w", encoding="utf-8")
                        file.write(f"{user.name}\n")
                        file = open(file_name, "a", encoding="utf-8")
                        for text_block in text_for_file.values():
                            for text in text_block:
                                if user.name == text[0] and message.channel == text[1]:
                                    file.write(
                                        f"{str(text[2])} :splitter: {str(text[3])}\n")
                        file.close()
bot.run(TOKEN)

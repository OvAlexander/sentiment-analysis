# This example requires the 'message_content' intent.

import discord
from dotenv import load_dotenv
import os
import datetime

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = False

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f"{guild.id} name: {guild.name}")


@bot.event
async def on_message(msg):
    channels = []
    channel_msgs = {}
    if msg.content == "hello":
        await msg.channel.send("merp")
    if msg.content == "scan":
        for guild in bot.guilds:
            # print(f"{guild.id} name: {guild.name}")
            for channel in guild.channels:
                channels.append(channel)
        # print(f"\n\n\n{channels}")
    # <Message id=1263125889642663967 channel=<TextChannel id=1262959409064317071 name='general' position=0 nsfw=False news=False category_id=1262959409064317069> type=<MessageType.default: 0> author=<Member id=1262958127532474440 name='TonySARk - IronBeaver' global_name=None bot=True nick=None guild=<Guild id=1262959409064317068 name='Testing Grounds' shard_id=0 chunked=False member_count=2>> flags=<MessageFlags value=0>>,
    for channel in channels:
        print(f"Channel: {channel.name} \n Type: {type(channel)}")
        if type(channel) == discord.channel.TextChannel:
            members = channel.members
            for member in members:
                if member.id == 1262958127532474440:
                    print("True")
                    messages = [message async for message in channel.history(limit=None)]
                    # print(messages)
                    channel_msgs[channel.name] = messages

    text_for_file = {}
    for channel_msg in channel_msgs.values():
        # print("#"*50)
        # print(type(channel_msg))
        # print(channel_msg)
        # print("#"*50)
        for message in channel_msg:
            user = message.author
            msg_id = message.id
            channel = message.channel
            text = message.content
            date = message.created_at
            date_formatted = date.ctime()
            print(
                f"In channel {message.channel} {user} sent message with id of {msg_id} on {date}:\n{text}")
            if user in text_for_file.keys():
                text_for_file[user].append(
                    (user.name, channel, text, date_formatted))
            else:
                text_for_file[user] = [
                    (user.name, channel, text, date_formatted)]

            for user in text_for_file:
                # print(user.display_name)
                # print(text_for_file[user])
                file_name = "./chat_logs/" + \
                    str(message.channel) + "_" + str(user) + ".txt"
                file = open(file_name, "w")
                file.write(f"{user.name}\n")
                file = open(file_name, "a")
                for text_block in text_for_file.values():
                    for text in text_block:
                        if user.name == text[0] and message.channel == text[1]:
                            file.write(
                                f"{str(text[2])} :splitter: {str(text[3])}\n")
                file.close()


bot.run(TOKEN)

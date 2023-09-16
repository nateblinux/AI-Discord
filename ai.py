import openai
import discord
import random
import os
from dotenv import load_dotenv
from bardapi import Bard

#load .env values
load_dotenv()
openai.api_key = os.getenv('OPEN_AI_KEY')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BARD_TOKEN = os.getenv('BARD_TOKEN')

#initialize messages for chatgpt:
messages=[{"role": "system", "content": "you have now been integrated into discord to act as a friendly chatbot"}]
#max characters that discord allows per message
DISCORD_MAX_CHARS = 2000

#initialize classes
client = discord.Client(intents=discord.Intents.default())
bard = Bard(token = BARD_TOKEN)

#connect to discord:
@client.event 
async def on_ready():
    print(f'{client.user.name} has connnected to Discord')

#on message recieve 
@client.event
async def on_message(message):
    global messages

    #dont respond to own messages or empty messages
    if message.author == client.user or not message.content:
        return
    
    print(message.content)

    ##OPENAI##
    await message.channel.send("Begin gpt response ")

    #track previous messages in conversation
    messages.append({"role": "user", "content": message.content})
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    print(chat_completion.choices[0].message.content)

    #discord max message length 2000 - break message into 2000 letter chunks 
    res_len = len(chat_completion.choices[0].message.content)

    if res_len > DISCORD_MAX_CHARS:
        sent_char = 0
        while sent_char < res_len:
            if (sent_char + DISCORD_MAX_CHARS) < res_len:
                await message.channel.send(chat_completion.choices[0].message.content[sent_char : sent_char+2000])
            else:
                await message.channel.send(chat_completion.choices[0].message.content[sent_char : res_len-1])

            sent_char+=DISCORD_MAX_CHARS
    else:
        await message.channel.send(chat_completion.choices[0].message.content)

    await message.channel.send("End gpt response ")

    ##BARD all logic same as gpt##
    await message.channel.send("Begin bard response ")

    chat = bard.get_answer(message.content)
    message_content = chat['content']
    print(message_content)

    res_len = len(message_content)

    if res_len > DISCORD_MAX_CHARS:
        sent_char = 0
        while sent_char < res_len:
            if (sent_char + DISCORD_MAX_CHARS) < res_len:
                await message.channel.send(message_content[sent_char : sent_char+2000])
            else:
                await message.channel.send(message_content[sent_char : res_len-1])

            sent_char+=DISCORD_MAX_CHARS
    else:
        await message.channel.send(message_content)

    await message.channel.send("End bard response ")

client.run(DISCORD_TOKEN)
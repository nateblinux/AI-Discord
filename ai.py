#!/usr/bin/env python
'''
Jobs for humanity discord bot for upskilling/language and housing support using chatgpt and/or google bard
Version: 0.0.1
Author: Nathan Benham
'''

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

#max characters that discord allows per message
DISCORD_MAX_CHARS = 2000

#initialize classes
client = discord.Client(intents=discord.Intents.default())
bard = Bard(token = BARD_TOKEN)

#PROMPT ENGINEERING STRINGS:
#initialize messages for chatgpt:
messages=[{"role": "system", "content": "Your job is to aid under represented communties find \
 jobs. You should answer questions as concisely as possible. Keep all responses under 1999 characters. \
 If you are asked a question about something other than spoken language courses or upskilling for jobs you should not answer. "}]

#header strings to append to each message:
gpt_prompt_header = "##INSTRUCTION## answer the following question in 2000 characters or less: question: "
bard_prompt_header = "##INSTRUCTION## Your role is to aid under represented communties find jobs by giving them support with. \
learning or improving their skills with spoken languages, and skills related to jobs. \
you answer questions about upskilling for jobs, as well as spoken langauge courses. \
You should answer questions as concisely as possible. Keep all responses under 600 characters.\
You must give resources to learn the skills that you suggest. Prioritize free and low cost courses. \
If you are asked a question about something other than spoken languages or upskilling for jobs you should not answer. \
You must give urls to any websites mentioned and contact information for any person mentioned. \
You must show the cost of the course. Display the information about courses in the following format:\
course name:, url or contact information for course:, cost:, course length:, online or in person\
you must include information for each of these fields. Prioritize online courses and couurses under $100 \
The question is surrounded by triple backticks. ```"

'''
Nate: 
1. Keep it short an structured
2. Must include link
3. Must include course length
4. Must include price
5. Price must be below $100 for the course
6. Must display if it's in person or online

DeQwon:
1. Start prompting bot
2. 75% of videos converted
3. Have a demo to show

Raghubir:
1. Integrate discord bot
2. Schedule meeting with julia
3. Prompt engineering
4. Have a demo to show
5. share with people and find out what is helpful


All:
Keep organized journal of:
bullet points for weeks
before we get to week 1
coalate all of the content into a course on LLM's
'''

#footer strings:
gpt_prompt_footer = ""
bard_prompt_footer = "```"

#DISCORD CONNECTION:

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

    #assemble prompt:
    prompt = gpt_prompt_header + message.content + gpt_prompt_footer

    print(prompt)

    #track previous messages in conversation
    messages.append({"role": "user", "content": prompt})
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

    prompt = bard_prompt_header + message.content + bard_prompt_footer

    print(prompt)

    chat = bard.get_answer(prompt)
    message_content = chat['content']
    print(chat)

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
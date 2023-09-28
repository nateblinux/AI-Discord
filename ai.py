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
from datetime import datetime

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
 jobs. You should answer questions as concisely as possible. Keep all responses under 600 characters. \
 If you are asked a question about something other than spoken language courses or upskilling for jobs you should not answer. "}]

#header strings to append to each message:
gpt_prompt_header = "##INSTRUCTION## answer the following question in 600 characters or less: question: "
bard_prompt_header = "##INSTRUCTION## Your role is to aid under represented communties find jobs by giving them support with. \
learning or improving their skills with spoken languages, and skills related to jobs. \
you answer questions about upskilling for jobs, as well as spoken langauge courses. \
You should answer as concisely as possible. Keep all responses under 600 characters.\
If you are asked a question about something other than spoken languages or upskilling for jobs you should not answer. \
First gather the following information about 3 - 7 courses that would be best for the user: 1. Course Name, 2. URL for course or contact information to sign up, \
3. Cost of course, 4. duration of course, 5. if the course is in person or online, 6. if in person course location. \
 You must give a response for each of these fields.\
 Prioritize free courses and courses under $100\
Give the response in the format: Course name, Course URL, Cost, Duration, Online or in person, location. Give these responses as bullet points\
Then give a recommendation to the user as to which of these courses would be best for them in 1 - 4 sentences. If the question seems like it is a follow\
up look at prevous questions to gain context and answer to the best of your ability. If the question seems to be simply a job description or resume you should ask how you can help ```"

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

#logging info:
file_name = "bot-log.txt"
log_file = open(file_name, "a")

def get_bard_response(prompt):
    try:
        chat = bard.get_answer(prompt)
        message_content = chat['content']
        print(chat)
        log_file.write(f'{prompt} \n {message_content} \n ----->')
        return message_content
    except Exception as err:
        return err

def get_gpt_response(prompt):
    global messages
    try:
        messages.append({"role": "user", "content": prompt})
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        return chat_completion.choices[0].message.content
    except Exception as err:
        return err

#DISCORD CONNECTION:

#connect to discord:
@client.event 
async def on_ready():
    print(f'{client.user.name} has connnected to Discord')

#on message recieve 
@client.event
async def on_message(message):

    #dont respond to own messages or empty messages
    if message.author == client.user or not message.content:
        return
    
    print(message.content)

    ##OPENAI##
    await message.channel.send("Begin gpt response ")

    #assemble prompt:
    prompt = gpt_prompt_header + message.content + gpt_prompt_footer
    print(prompt)
    await message.channel.send(get_gpt_response(prompt))
    await message.channel.send("End gpt response ")

    ##BARD all logic same as gpt##
    await message.channel.send("Begin bard response ")
    prompt = bard_prompt_header + message.content + bard_prompt_footer
    print(prompt)    
    await message.channel.send(get_bard_response(prompt))

    await message.channel.send("End bard response ")

client.run(DISCORD_TOKEN)
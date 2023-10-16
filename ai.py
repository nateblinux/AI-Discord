#!/usr/bin/env python
'''
Jobs for humanity discord bot for upskilling/language and housing support using chatgpt and/or google bard
Version: 0.1.0
Author: Nathan Benham
'''

import openai
import discord
import random
import os
from dotenv import load_dotenv
import bardapi
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

#PROMPT ENGINEERING STRINGS:

#store context for bard to allow for multiple messages
#format for context dictionary userId:[messageHistory]
bard_context = {}

#header strings to append to each message:
gpt_prompt_header = "##INSTRUCTION## define the type of the following prompt as either a question or none. \
Give your response in the following format \'{class: type}\' do not give any other information. The prompt is surrounded by triple backticks. ```"

bard_prompt_header = "##INSTRUCTION## Your role is to aid under represented communties find jobs by giving them support with. \
learning or improving their skills with spoken languages, and skills related to jobs. \
if you are asked a question about spoken languages or upskilling classes you must answer to the best of your ability.\
If you are asked a question about something other than finding classes do not answer.\
Keep all responses under 600 characters. \
Gather the following information about 2 - 4 courses that would be best for the user: 1. Course Name, 2. URL for course or contact information to sign up, \
3. Cost of course, 4. duration of course, 5. if the course is in person or online, 6. if in person course location. \
You must give a response for each of these fields, The URL must be a valid address.\
Prioritize free courses and courses under $100\
Give the response in the format: -Course name\n -Course URL\n -Cost\n -Duration\n -Online or in person\n -location\n. Give these responses as bullet points\
Then give a recommendation to the user as to which of these courses would be best for them in 1 - 2 sentences. The users query is surrounded by triple backticks.```"

#footer strings:
gpt_prompt_footer = "```"
bard_prompt_footer = "```"

#logging info:
file_name = "bot-log.txt"
log_file = open(file_name, "a")

def get_bard_response(prompt):
    try:
        chat = bardapi.core.Bard(BARD_TOKEN).get_answer(prompt)
        message_content = chat['content']
        print(chat)
        log_file.write(f'{prompt} \n {message_content} \n ----->')
        return message_content
    except Exception as err:
        return err

def get_gpt_response(prompt):
    global messages
    try:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=prompt)
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

    #reset command for message history
    if(message.content == "/reset"):
        if(message.author.id in bard_context):
            del bard_context[message.author.id]
            await message.channel.send(f"<@{message.author.id}> Your conversation has been reset")
            return
        else:
            await message.channel.send(f"<@{message.author.id}> You have no conversation history")
            return

    #add to message history
    if(message.author.id in bard_context):
        bard_context[message.author.id].append(message.content)
    else:
        bard_context.update({message.author.id:[message.content]})

    #print(bard_context[message.author.id])

    #convert history array to string
    prompt_str = ' '.join(bard_context[message.author.id])

    #pop oldest messages from history
    while(len(prompt_str) > 4000):
        bard_context[message.author.id].pop(0)
        prompt_str = ' '.join(bard_context[message.author.id])
    
    #print(prompt_str)

    #classify the prompt as either question or none:
    prompt_class = get_gpt_response([{"role" : "user", "content" : gpt_prompt_header + message.content + gpt_prompt_footer}])

    #print(prompt_class)

    #if gpt classifies prompt as question:
    if("question" in prompt_class):
        prompt = bard_prompt_header + prompt_str + bard_prompt_footer
        #print(prompt)   

        #try catch for bard response 
        try: 
            #get response, add to context, send message to user
            bard_res = get_bard_response(prompt)
            bard_context[message.author.id].append(bard_res)
            await message.channel.send(f"<@{message.author.id}> {bard_res}")
        except Exception as err:
            #tell user if there was an error
            await message.channel.send(f"<@{message.author.id}> There was an error: {err}")

    #if not question send static message 
    else:
        await message.channel.send(f"<@{message.author.id}> That does not appear to be a question but I will remember it for future answers. Keep in mind I can only process about 4000 characters 
        So I only know our most recent messages. You can reset your conversation history with /reset ")


client.run(DISCORD_TOKEN)
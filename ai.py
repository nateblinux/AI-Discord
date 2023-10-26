#!/usr/bin/env python
'''
Jobs for humanity discord bot for upskilling/language and housing support using PaLM
Author: Nathan Benham
'''
import discord
import random
import os
from dotenv import load_dotenv
import google.generativeai as palm

#load .env values
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PALM_KEY = os.getenv('PALM_KEY')

#token limit for PaLM text-bison-001 (1 token ~= 4 chars 8196 tokens max)
TOKEN_LIMIT = 8000 * 4
#initialize classes
client = discord.Client(intents=discord.Intents.default())

palm.configure(api_key=PALM_KEY)


#PROMPT ENGINEERING STRINGS:

#store context for text-bison to allow for multiple messages
#format for context dictionary userId:[messageHistory]
bot_users = {}

#header strings to append to each message:
palm_prompt_header = "##INSTRUCTION## Your role is to aid under represented communties find jobs by giving them support with. \
learning or improving their skills with spoken languages, and skills related to jobs. \
if you are asked a question about spoken languages or upskilling classes you must answer to the best of your ability.\
If you are asked a question about something other than finding classes do not answer.\
Keep all responses under 600 characters. \
Gather the following information about 2 - 4 courses that would be best for the user: 1. Course Name, 2. URL for course or contact information to sign up, \
3. Cost of course, 4. duration of course, 5. if the course is in person or online, 6. if in person course location. \
You must give a response for each of these fields, The URL must be a valid address.\
Prioritize free courses and courses under $100\
Give the response in the format: -Course name\n -Course URL\n -Cost\n -Duration\n -Online or in person\n -location\n. Give these responses as bullet points\
Then give a recommendation to the user as to which of these courses would be best for them in 1 - 2 sentences. The users conversation is surrounded by triple backticks.\
The parts of the query may contain previous bot responses labeled as bot responded, The users questions are labeled as user asked. Do not say bot responded or user asked\
in your response```"



#footer strings:
palm_prompt_footer = "```"

#logging info:
file_name = "bot-log.txt"
log_file = open(file_name, "a")


#get the palm response temperature 0 means no creativity
def get_palm_response(prompt):
    global palm_users
    try:
        response = palm.generate_text(
            model='models/text-bison-001',
            prompt=prompt,
            temperature=0
        )
        print(response)
        return response.result
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

    user_tag = ""

    #dont respond to own messages or empty messages
    if message.author == client.user or not message.content:
        return

    #dont tag user in private channel ie DMing bot
    if(message.channel.type != discord.ChannelType.private):
        user_tag = f"<@{message.author.id}>"
        

    #reset command for message history
    if(message.content == "/reset"):
        if(message.author.id in bot_users):
            del bot_users[message.author.id]
            await message.channel.send(f"{user_tag} Your conversation has been reset")
            return
        else:
            await message.channel.send(f"{user_tag} You have no conversation history")
            return


    #add message to user history
    if message.author.id in bot_users: 
        bot_users[message.author.id].append(f"user asked: {message.content},")
    else:
        bot_users.update({message.author.id:[f"user asked: {message.content},"]})

    print(bot_users)
    ##palm test code

    #convert array for history to string
    context_str = ' '.join(bot_users[message.author.id])

    #keep context under token limit by deleting oldest messages + regenerating string
    while(len(context_str) > TOKEN_LIMIT):
        try:
            bot_users[message.author.id].pop(0)
            bot_users[message.author.id].pop(1)
            context_str = ' '.join(bot_users[message.author.id])
        except:
            await message.channel.send(f"{user_tag} There was an error try /reset to reset your conversation")

    #create prompt and get response
    prompt = palm_prompt_header + context_str + palm_prompt_footer
    bot_res = get_palm_response(prompt)

    #add response to message history
    bot_users[message.author.id].append(f"bot responded: {bot_res},")

    #message user bot response
    await message.channel.send(f"{user_tag}{bot_res}")


client.run(DISCORD_TOKEN)
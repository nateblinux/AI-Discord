#!/usr/bin/env python
'''
Jobs for humanity discord bot for upskilling/language and housing support using chatgpt and/or google bard
Version: 0.0.1
Author: Nathan Benham
'''
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.chains import ConversationChain  
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper

#load .env values
load_dotenv()
api_key = os.getenv('OPEN_AI_KEY')
google_cse = os.getenv('GOOGLE_CSE')
google_api = os.getenv('GOOGLE_API')

chat = ChatOpenAI(openai_api_key=api_key)
search = GoogleSearchAPIWrapper(google_api_key=google_api, google_cse_id=google_cse)

tool = Tool(
    name="Google Search",
    description="Search Google for classes",
    func=search.run,
)

def get_results(query):
    return search.results(query, 3)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "Your role is to help people find courses to upskill for jobs including spoken language courses. \
             First you must analyze the question asked to determine skill gaps, Then you must formulate a google search to best find courses for that user to fill in those skill gaps.\
             only give a google search \
             with no extra information"
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)

conversation = LLMChain(llm=chat, prompt=prompt, verbose=True, memory=memory)

print(get_results("online java classes for job upskilling"))

while(True):
    inp = input(">> ")
    result = conversation({"question" : inp})
    print(result['text'])

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

#load .env values
load_dotenv()
api_key = os.getenv('OPEN_AI_KEY')

chat = ChatOpenAI(openai_api_key=api_key)

prompt = ChatPromptTemplate(
    messages=[
        SystemMessagePromptTemplate.from_template(
            "You are a nice chatbot having a conversation with a human."
        ),
        # The `variable_name` here is what must align with memory
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{question}")
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)

conversation = LLMChain(llm=chat, prompt=prompt, verbose=True, memory=memory)

while(True):
    inp = input(">> ")
    result = conversation({"question" : inp})
    print(result['text'])

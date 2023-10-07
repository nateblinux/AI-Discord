Discord bot for gpt

requires:
python3
openai
discord.py
dotenv
bardapi
langchain
google api client

Steps to run:
1. create venv: python -m venv path/to/venv
2. use venv: source path/to/venv/bin/activate
3. install libaries: 
    - pip install openai
    - pip install discord.py
    - pip install dotenv
    - pip install langchain
    - pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
4. rename .env.example to .env
    - replace openai api key and discord token with your keys
5. run: python ai.py
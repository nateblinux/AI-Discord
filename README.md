Discord bot for gpt

requires:
python3
discord.py
dotenv
bardapi

Steps to run:
1. create venv: python -m venv path/to/venv
2. use venv: source path/to/venv/bin/activate
3. install libaries: 
    - pip install google-generativeai
    - pip install discord.py
    - pip install dotenv
4. rename .env.example to .env
    - replace palm api key and discord token with your keys
5. run: python ai.py
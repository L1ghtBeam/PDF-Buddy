from sys import exit

from dotenv import load_dotenv
from openai import OpenAI

from pdf_buddy.assistant import get_assistant
from pdf_buddy.chat import start_chat


def main():
    print("Running")
    # vscode will use .env files automatically, but cmd wont so this is 
    # necessary to load our api key in all cases
    load_dotenv()
    client = OpenAI()

    assistant = get_assistant(client)
    if not assistant:
        exit()
    
    start_chat(client, assistant)
from openai import OpenAI
from dotenv import load_dotenv
from pdf_buddy.menu import get_assistant
from sys import exit


def main():
    print("Running")
    # vscode will use .env files automatically, but cmd wont so this is 
    # necessary to load our api key in all cases
    load_dotenv()
    client = OpenAI()

    assistant = get_assistant(client)
    if not assistant:
        exit()
    
    print(assistant.name or "Untitled",
          assistant.description or "No description",
          assistant.id, sep=' | ')
import os
from pathlib import Path
from sys import exit

from dotenv import load_dotenv
from openai import OpenAI

from pdf_buddy.assistant import get_assistant
from pdf_buddy.chat import start_chat


def main() -> None:
    print("Running")
    # some IDEs will use .env files automatically, but cmd won't so this is
    # necessary to load our api key in all cases
    load_dotenv()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: The OPENAI_API_KEY environment variable could not be"
              " found!")
        create_sample_env_file(Path() / '.env')
        exit(1)
        return
    client = OpenAI(api_key=api_key)

    assistant = get_assistant(client)
    if not assistant:
        exit()

    start_chat(client, assistant)


def create_sample_env_file(file_path: Path) -> None:
    if file_path.exists():
        return

    try:
        with file_path.open('x') as f:
            f.write("OPENAI_API_KEY=\n")
    except OSError as e:
        print(f"Could not create a .env file!\nError {e.errno}: {e.strerror}.")
    else:
        print(f"Created a sample .emv file at {file_path.resolve()}. Please"
              f" enter your OpenAI API key after the phrase 'OPENAI_API_KEY='"
              f" in the file and try again.")

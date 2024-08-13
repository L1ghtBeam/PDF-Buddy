from openai import OpenAI
from openai.types.beta.assistant import Assistant
from typing import Optional


def get_assistant(client: OpenAI) -> Optional[Assistant]:
    print("Available Buddys:")
    all_assistants = []
    for i, assistant in enumerate(client.beta.assistants.list(
        order='desc',
        limit=20
    )):
        print(f"  {i:<2} {(assistant.name or 'Untitled buddy')}")
        all_assistants.append(assistant)
    
    print(f"  {i+1:<2} Create new buddy")

    print("\nChoose an option above or [q]uit")

    while True:
        user_input = input()
        if user_input[0].strip().lower() == 'q':
            return None
        try:
            user_val = int(user_input)
        except ValueError:
            print("Invalid value!")
            continue
        
        if not 1 <= user_val <= len(all_assistants) + 1:
            print("Not an option!")
            continue

        if 1 <= user_val <= len(all_assistants):
            return all_assistants[user_val - 1]
        else:
            return create_assistant(client)


def create_assistant(client: OpenAI) -> Assistant:
    # TODO: create a new assistant from scratch
    raise NotImplementedError()
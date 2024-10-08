from openai import OpenAI, APIStatusError
from openai.types.beta.assistant import Assistant
from typing import Optional

DEFAULT_MODEL = 'gpt-4o-mini'
DEFAULT_INSTRUCT = "You are a studying assistant for the user. Use the provided"\
                 " study materials in order to answer questions."


def get_assistant(client: OpenAI) -> Optional[Assistant]:
    print("Available Buddies:")
    all_assistants: list[Assistant] = []
    for i, assistant in enumerate(client.beta.assistants.list(
        order='desc',
        limit=20
    )):
        print(f"  {i+1:<2} {(assistant.name or 'Untitled buddy')}")
        all_assistants.append(assistant)
    
    print(f"  {i+2:<2} Create new buddy")

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
    try:
        print("Creating a new buddy\nCTRL + C at any time to cancel")
        assistant: Optional[Assistant] = None
        while not assistant:
            
            name = input("Assistant name: ").strip()
            desc = input("Description (optional): ").strip()

            recommended_models = ['gpt-4o', 'gpt-4o-mini']
            print("Enter an OpenAI model to use. Recommended models include: ")
            for rec in recommended_models:
                print(f"  {rec}")
            print('\ngpt-4o-mini will be used if no model is selected')
            model = input("Model: ").strip().lower() or DEFAULT_MODEL

            if model not in recommended_models:
                print("Warning! Selected model is not a recommended model.",
                      "Issues may occur")
            
            print("Enter instructions for your study buddy. Instructions tell",
                  "your study buddy how to answer questions. Good",
                  "instructions should:\n  (1) instruct the program to be",
                  "helpful by answering questions\n  (2) inform the program",
                  "of the subject of the study\n  (3) tell the program what",
                  "type of files it will have access to")
            print(f"\nDefault instructions: {DEFAULT_INSTRUCT}")
            print("The default instructions will be used if no instructions",
                  "are entered, but it's highly recommended to write your own.")
            instruct = input("Instructions: ").strip() or DEFAULT_INSTRUCT

            print("\nYour study buddy:"
                  f"\n  name: {name}"
                  f"\n  description: {desc}"
                  f"\n  model: {model}"
                  f"\n  instructions: {instruct}")

            while True:
                print("\nPlease [c]onfirm, [r]edo, or [q]uit your selection")
                option = input().strip().lower()
                if len(option) and option[0] in ['c', 'r', 'q']:
                    break
                print("Invalid option!")
            
            if option == 'q':
                return None
            if option == 'r':
                print()
                continue
            
            try:
                assistant = client.beta.assistants.create(
                    model=model,
                    name=name,
                    description=desc,
                    instructions=instruct,
                    tools=[{"type": "file_search"}]
                )
            except APIStatusError as e:
                print(f"Error {e.status_code}! {e.body['message']}\n")

    except KeyboardInterrupt:
        print("\nCTRL + C pressed! Cancelling buddy creation")
        return None
    else:
        return assistant
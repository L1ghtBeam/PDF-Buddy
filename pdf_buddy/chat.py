from openai import APIConnectionError, AssistantEventHandler, OpenAI
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta
from typing_extensions import override


# EventHandler class from OpenAI docs to define how we want to handle the
# events in the response stream.
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text: Text) -> None:
        print(f"\nbuddy> ", end='', flush=True)

    @override
    def on_text_delta(self, delta: TextDelta, snapshot: Text) -> None:
        print(delta.value, end='', flush=True)

    def on_tool_call_created(self, tool_call: ToolCall) -> None:
        if tool_call.type == 'file_search':
            print(f"\nbuddy> Searching my files...", flush=True)
        else:
            print(f"\nbuddy> {tool_call.type}", flush=True)

    # not currently used
    def on_tool_call_delta(self, delta: ToolCallDelta,
                           snapshot: ToolCall) -> None:
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end='', flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == 'logs':
                        print(f"\n{output.logs}", flush=True)


def get_thread(client: OpenAI) -> Thread:
    # TODO: get threads history from a locally saved memory
    # for now, create a new thread automatically

    return client.beta.threads.create()


def start_chat(client: OpenAI, assistant: Assistant) -> int:
    thread = get_thread(client)

    print(f"Chat started with {assistant.name or "Untitled buddy"}\n"
          "CTRL + C to stop the conversation at any time")
    
    while True:
        try:
            chat_loop(client, assistant, thread)
        except KeyboardInterrupt:
            print("\nCTRL + C pressed. Goodbye!")
            return 0
        except APIConnectionError:
            print("\nA connection error has occurred. Try again later")


def chat_loop(client: OpenAI, assistant: Assistant, thread: Thread) -> None:
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=input('\nyou> ')
    )

    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler(),
    ) as stream:
        stream.until_done()
    print()
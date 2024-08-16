from openai import APIConnectionError, AssistantEventHandler, OpenAI
from openai.types import FileObject
from openai.types.beta.assistant import Assistant
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.runs import ToolCall, ToolCallDelta
from typing_extensions import override


# EventHandler class from OpenAI docs to define how we want to handle the
# events in the response stream.
class EventHandler(AssistantEventHandler):

    def __init__(self, client: OpenAI, name: str = '') -> None:
        super().__init__()
        self.name = name or "buddy"
        self.client = client
        # citations list to be filled whenever necessary
        self.citations: list[dict[str, str]]

    @override
    def on_text_created(self, text: Text) -> None:
        print(f"\n{self.name}> ", end='', flush=True)
        self.citations = []

    @override
    def on_text_delta(self, delta: TextDelta, snapshot: Text) -> None:
        delta_content = delta.value
        if not delta_content:
            return

        if annotations := delta.annotations:
            for annotation in annotations:
                delta_content = delta_content.replace(
                    annotation.text, f"[{len(self.citations)+1}]"
                )
                self.citations.append({'type': annotation.type})
                if file_citation := getattr(annotation, "file_citation", None):
                    self.citations[-1]['file_id'] = file_citation.file_id
                    
        print(delta_content, end='', flush=True)

    @override
    def on_tool_call_created(self, tool_call: ToolCall) -> None:
        if tool_call.type == 'file_search':
            print(f"\n{self.name}> Searching my files...", flush=True)
        else:
            print(f"\n{self.name}> {tool_call.type}", flush=True)

    # not currently used
    @override
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
    
    @override
    def on_text_done(self, text: Text) -> None:
        print()
        if not self.citations:
            return
        
        print("\nCitations:")
        file_cache: dict[str, FileObject] = {}
        for i, citation in enumerate(self.citations):
            if citation['type'] == 'file_citation':
                file_id = citation['file_id']
                file = file_cache.get(file_id, self.client.files.retrieve(
                    file_id
                ))
                file_cache[file_id] = file
                cite = file.filename
            else:
                cite = citation['type']

            print(f"  [{i+1}] {cite}")


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
    user_input = input('\nyou> ').strip()
    if not user_input:
        return

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler(client, assistant.name),
    ) as stream:
        stream.until_done()